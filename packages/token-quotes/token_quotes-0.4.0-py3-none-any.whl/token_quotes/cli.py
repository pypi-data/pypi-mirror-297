import argparse
import asyncio
import logging
import os
from pathlib import Path

from dotenv import load_dotenv

from .wallet_manager_latest import WalletManager

logger = logging.getLogger(__name__)


async def run_wallet_manager(input_file: Path, compress_output: bool, wallet_manager: WalletManager):
    # Paths to cache files
    balances_file = Path("balances.json")
    portfolios_file = Path("portfolios.json")

    # Load cached data from disk
    wallet_manager.load_balances_from_disk(balances_file)
    wallet_manager.load_portfolios_from_disk(portfolios_file)

    # Fetch balances and portfolio data
    balance_results = await wallet_manager.fetch_all_balances("USD")
    portfolio_results = await wallet_manager.fetch_daily_portfolio_balances("USD")

    # Save data to disk
    wallet_manager.save_balances_to_disk(balances_file, compress=compress_output)
    wallet_manager.save_portfolios_to_disk(portfolios_file, compress=compress_output)

    # Pretty printing output
    print("\n" + "=" * 50)
    print("Token Quotes Wallet Manager Run Summary")
    print("=" * 50)

    print(f"\nInput file: {input_file}")
    print(f"Cache TTL: {wallet_manager.cache_ttl} seconds")
    print(f"Number of wallets loaded: {len(wallet_manager.wallets)}")

    print("\nWallets:")
    for wallet in wallet_manager.wallets:
        print(f"{wallet}\n")

    # Simplified and consistent fetch summary and error reporting
    print("\nFetch Summary:")
    balance_success = sum(1 for result, _ in balance_results if isinstance(result, dict))
    portfolio_success = sum(1 for result, _ in portfolio_results if isinstance(result, dict))
    balance_errors = len(balance_results) - balance_success
    portfolio_errors = len(portfolio_results) - portfolio_success

    print("  Balances:")
    print(f"    Successful: {balance_success}")
    print(f"    Failed: {balance_errors}")
    print("  Portfolio balances:")
    print(f"    Successful: {portfolio_success}")
    print(f"    Failed: {portfolio_errors}")

    total_errors = balance_errors + portfolio_errors
    if total_errors > 0:
        print(f"\nTotal errors encountered: {total_errors}")
        print("\nDetailed Error Information:")
        for data_type, results in [("balance", balance_results), ("portfolio", portfolio_results)]:
            for result, info in results:
                if isinstance(result, Exception) or result is None:
                    print(f"  Error fetching {data_type}:")
                    print(f"    Wallet: '{info['wallet_name']}'")
                    print(f"    Address: '{info['address']}'")
                    print(f"    Chain ID: '{info['chain_id']}'")
                    print(f"    Details: {str(result) if isinstance(result, Exception) else 'No data returned'}")
                    print()

    print("\n" + "=" * 50)
    print("End of Token Quotes Wallet Manager Run")
    print("=" * 50)


def main():
    load_dotenv()

    parser = argparse.ArgumentParser(description="Wallet Manager")
    parser.add_argument("--input", type=str, required=True, help="Path to the input YAML file")
    parser.add_argument("--api_key", type=str, default=os.getenv("COVALENT_API_KEY"), help="Covalent API Key")
    parser.add_argument(
        "--log_level",
        type=str,
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Logging level",
    )
    parser.add_argument("--compress", action="store_true", help="Compress output files using gzip")
    args = parser.parse_args()

    api_key = args.api_key

    if not api_key:
        logger.error("Error: Covalent API Key is required.")
        exit(1)

    input_file = Path(args.input)
    if not input_file.is_file():
        logger.error(f"Error: Input file {input_file} does not exist.")
        exit(1)

    # Set cache TTL (e.g., 300 seconds)
    cache_ttl = 300
    wallet_manager = WalletManager(api_key, cache_ttl=cache_ttl)
    wallet_manager.load_wallets(input_file)

    # Run the main function
    asyncio.run(run_wallet_manager(input_file, args.compress, wallet_manager))


if __name__ == "__main__":
    main()
