import argparse
import asyncio
import json
import logging
from pathlib import Path
from pprint import pformat
import typing

import eth_account
from eth_account.signers.local import LocalAccount
from mach_client import client, Token

from .aave import aave_test
from .balances import get_balances
from .destination_policy import (
    DestinationPolicy,
    RandomChainFixedSymbolPolicy,
    RandomChainRandomSymbolPolicy,
)
from .log import make_logger
from .mach import mach_test
from .utility import choose_source_token
from .withdraw import drain_all


USAGE = """
cctt generate --password PASSWORD
    Generate a random ETH public-private key-pair. Outputs the public key and writes the encrypted account to the account file.
    Warning: overwrites existing account file. This is irreversible.

cctt import --password PASSWORD --private-key PRIVATE_KEY
    Import an existing account corresponding to the given private key. Outputs the public key and writes the encrypted account to the account file.
    Warning: overwrites existing account file. This is irreversible.

cctt decrypt --password PASSWORD
    Display the public-private key pair in the account file, decrypted with the password.

cctt balances
    Display balances of all tokens on all supported chains.

cctt run --password PASSWORD --source arbitrum-USDC --destination USDC
    Perform the test using the account in the account file. 
    The first trade is made from the chain and symbol specified by the --source argument.
    In each trade, a random chain is chosen as the destination chain and the entire balance of the source token is sold for the destination token.
    The choice of destination token is controlled by the --destination argument.
    In the next trade, the destination token becomes the new source token.
    This repeats until the program is stopped.

    Note: currently does not support trading the gas token (ETH) on any chain.

cctt aave --passowrd PASSWORD
    Run the AAVE testing script. Constantly moves balances between the highest interest pool every 5 minutes.
    Currently uses USDC, USDT, FRAX and DAI on all supported chains.
    If the current pool is the best pool, will instead switch to the second best pool.

cctt withdraw --password PASSWORD -wallet WALLET
    Withdraw all tokens and gas (ETH) on all supported chains from the account into the provided wallet address.
"""

DESCRIPTION = "Cross chain trade test (CCTT) - test swaps between random chains"

DEFAULT_ACCOUNT_FILEPATH = Path("account.json")

DEFAULT_SOURCE_TOKEN = Token("arbitrum-USDC")

DEFAULT_DESTINATION_POLICY = "USDC"

SOURCE_TOKEN_DESCRIPTION = f"""
The initial token to be sold in the first trade in the form of chain-SYMBOL, defaulting to {DEFAULT_SOURCE_TOKEN}.
If explicitly nulled out, ie. --source with no argument, then a random viable source token will be chosen for you.
"""

DESTINATION_POLICY_DESCRIPTION = f"""
Controls how the destination token is chosen in each trade.
If set to "random", then a completely random chain and symbol will be chosen.
If set to "fixed:SYMBOL", then a token on a random chain with the given symbol will be chosen.
Defaults to {DEFAULT_DESTINATION_POLICY}.
"""


def load_account(account_filepath: Path) -> dict:
    with open(account_filepath, "r") as account_file:
        encrypted = json.load(account_file)
    return encrypted


# Returns the account object
def read_account(password: str, account_filepath: Path) -> LocalAccount:
    encrypted = load_account(account_filepath)
    decrypted = eth_account.Account.decrypt(encrypted, password)
    account = eth_account.Account.from_key(decrypted)

    return account


# Writes an encrypted account
def write_account(encrypted: dict, account_filepath: Path) -> None:
    with open(account_filepath, "w") as account_file:
        account_file.write(json.dumps(encrypted))


async def run() -> None:
    logger = logging.getLogger("cctt")

    parser = argparse.ArgumentParser(
        prog="cctt",
        usage=USAGE,
        description=DESCRIPTION,
    )

    parser.add_argument(
        "command",
        choices=(
            "generate",
            "import",
            "decrypt",
            "balances",
            "run",
            "aave",
            "withdraw",
        ),
        help="Command to perform",
        nargs=1,
        type=str,
    )

    parser.add_argument(
        "--private-key",
        "-k",
        dest="private_key",
        help="Hex private key of the account you'd like to import",
        nargs="?",
        required=False,
        type=str,
    )

    parser.add_argument(
        "--password",
        "-p",
        dest="password",
        help="Password used to encrypt/decrypt the private key",
        nargs="?",
        required=False,
        type=str,
    )

    parser.add_argument(
        "--wallet",
        "-w",
        dest="wallet",
        help="Hex destination wallet address for withdrawal",
        nargs="?",
        required=False,
        type=str,
    )

    parser.add_argument(
        "--file",
        "-f",
        default=DEFAULT_ACCOUNT_FILEPATH,
        dest="account_filepath",
        help=f"Path to the JSON file storing the encrypted account data, defaulting to {DEFAULT_ACCOUNT_FILEPATH}",
        required=False,
        nargs="?",
        type=Path,
    )

    parser.add_argument(
        "--source",
        "-s",
        default=DEFAULT_SOURCE_TOKEN,
        dest="src_token",
        help=SOURCE_TOKEN_DESCRIPTION,
        required=False,
        nargs="?",
        type=Token,
    )

    parser.add_argument(
        "--destination-policy",
        "-d",
        default=DEFAULT_DESTINATION_POLICY,
        dest="destination_policy",
        help=DESTINATION_POLICY_DESCRIPTION,
        required=False,
        nargs="?",
        type=str,
    )

    arguments = parser.parse_args()

    command: str = arguments.command[0]
    assert command, "Command required"
    account_filepath: Path = arguments.account_filepath
    assert account_filepath, "Account filepath required"

    if command == "balances":
        # Wallet address is unencrypted, don't need password
        encrypted = load_account(account_filepath)
        wallet = f"0x{encrypted['address']}"
        balances = get_balances(wallet)
        logger.info("Balances:")
        logger.info(pformat(balances))

        return

    password: str = arguments.password
    assert password, "Password required"

    match command:
        case "generate":
            account = eth_account.Account.create()

        case "import":
            private_key = arguments.private_key
            assert private_key, "Private key must be provided to import wallet"
            account = eth_account.Account.from_key(private_key)

        case _:
            account = read_account(password, account_filepath)

    logger.info(f"Public key: {account.address}")

    match command:
        case "generate" | "import":
            encrypted = account.encrypt(password)
            write_account(encrypted, account_filepath)

        case "decrypt":
            print(f"Private key: {account.key.hex()}")

        case "run":
            src_token = (
                arguments.src_token
                if arguments.src_token
                else choose_source_token(frozenset(), account.address)
            )
            assert (
                src_token.symbol not in client.gas_tokens.values()
            ), "Cannot trade the gas token"

            logger.info(f"Source token: {src_token}")

            assert (
                arguments.destination_policy
            ), "Destination policy must be provided to run test"

            if arguments.destination_policy == "random":
                logger.info("Destination token policy: randomize")
                destination_policy: DestinationPolicy = RandomChainRandomSymbolPolicy()
            else:
                policy, symbol = arguments.destination_policy.split(":")
                assert (
                    policy == "fixed"
                ), f"Unrecognized destination token policy: {policy}"

                logger.info(f"Destination token policy: fixed symbol {symbol}")
                destination_policy: DestinationPolicy = RandomChainFixedSymbolPolicy(symbol)  # type: ignore

            await mach_test.run(src_token, destination_policy, account)

        case "aave":
            await aave_test.run(account)

        case "withdraw":
            wallet = arguments.wallet
            assert wallet, "Destination wallet must be provided for withdrawal"

            await drain_all(account, wallet)

        case _ as unreachable:
            typing.assert_never(unreachable)  # type: ignore


def main() -> None:
    if __name__ == "__main__":
        make_logger("cctt", True, Path("app.log"))

        # Silence annoying aiohttp warning about unclosed client session originating from web3's code
        logging.getLogger("asyncio").setLevel(logging.CRITICAL)

    asyncio.run(run())
