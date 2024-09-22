import asyncio
import gzip
import json
import logging
import time
from dataclasses import dataclass, field
from enum import StrEnum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

import yaml
from cachetools import TTLCache

from .api_clients import AsyncCovalentClient, CovalentAPIError

# Create a logger instance for this module
logger = logging.getLogger(__name__)


@dataclass
class WalletAddress:
    address: str
    chain_ids: List[str]
    owner: str
    purpose: str

    def __str__(self):
        return (
            f"Address: {self.address[:6]}...{self.address[-4:]} | "
            f"Chains: {', '.join(self.chain_ids)} | "
            f"Owner: {self.owner} | "
            f"Purpose: {self.purpose}"
        )


@dataclass
class Wallet:
    name: str
    metadata: Dict[str, Any]
    addresses: List[WalletAddress] = field(default_factory=list)

    def __str__(self):
        address_str = "\n    ".join(str(addr) for addr in self.addresses)
        return f"Wallet: {self.name}\n  Metadata: {self.metadata}\n  Addresses:\n    {address_str}"


class DataType(StrEnum):
    BALANCE = "balance"
    PORTFOLIO = "portfolio"


class WalletManager:
    """Manages wallet information and token balance fetching."""

    def __init__(self, api_key: str, cache_ttl: int = 3000):
        self.client = AsyncCovalentClient(api_key)
        self.cache_ttl = cache_ttl
        self.balances_cache: TTLCache[Tuple[str, str, str], Dict[str, Any]] = TTLCache(maxsize=1000, ttl=cache_ttl)
        self.portfolios_cache: TTLCache[Tuple[str, str, str], Dict[str, Any]] = TTLCache(maxsize=1000, ttl=cache_ttl)
        self.balances: List[Dict[str, Any]] = []
        self.portfolios: List[Dict[str, Any]] = []
        self.wallets: List[Wallet] = []

    def load_wallets(self, input_source: Path):
        """Load wallet information from a YAML file and store in self.wallets."""
        if not isinstance(input_source, Path):
            raise TypeError("input_source must be a pathlib.Path instance")

        if not input_source.is_file():
            raise ValueError(f"Input source is not a file: {input_source}")

        if input_source.suffix not in [".yaml", ".yml"]:
            raise ValueError(f"Unsupported file type: {input_source.suffix}. Only YAML files are supported.")

        logger.info(f"Loading wallets from YAML file: {input_source}")
        try:
            data = yaml.safe_load(input_source.read_text())
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML file: {input_source}") from e

        if not isinstance(data, dict) or "wallets" not in data:
            raise ValueError("Invalid YAML structure. Expected a 'wallets' key at the root level.")

        wallets_data = data["wallets"]
        wallets = []
        for wallet_data in wallets_data:
            addresses = [
                WalletAddress(
                    address=addr.get("address"),
                    chain_ids=addr.get("chain_ids", []),
                    owner=addr.get("owner"),
                    purpose=addr.get("purpose"),
                )
                for addr in wallet_data.get("addresses", [])
            ]
            wallet = Wallet(
                name=wallet_data.get("name"),
                metadata=wallet_data.get("metadata", {}),
                addresses=addresses,
            )
            wallets.append(wallet)

        logger.debug(f"Loaded wallets: {wallets}")
        self.wallets = wallets

        # Print loaded wallets
        print("\nLoaded Wallets:")
        for wallet in self.wallets:
            print(f"{wallet}\n")

    async def _fetch_data(
        self,
        wallet: Wallet,
        address_info: WalletAddress,
        chain_id: str,
        quote_currency: str,
        data_type: str,
    ) -> Optional[Dict[str, Any]]:
        """Generic method to fetch data (balance or portfolio) and cache the result."""
        cache = self.balances_cache if data_type == DataType.BALANCE.value else self.portfolios_cache
        cache_key = (address_info.address, chain_id, quote_currency)

        if cache_key in cache:
            logger.debug(f"Cache hit for {data_type} of address {address_info.address} " f"on chain {chain_id}")
            data = cache[cache_key]
        else:
            try:
                if data_type == DataType.BALANCE.value:
                    response = await self.client.get_token_balances(chain_id, address_info.address, quote_currency)
                else:
                    response = await self.client.get_daily_portfolio_balances(
                        chain_id, address_info.address, quote_currency, days=2
                    )
                if response["success"]:
                    data = response["data"]
                    # Add timestamp to the cached data
                    data["timestamp"] = time.time()
                    cache[cache_key] = data
                    logger.debug(
                        f"Fetched {data_type} from API for address {address_info.address} " f"on chain {chain_id}"
                    )
                else:
                    logger.error(
                        f"API error for {address_info.address} on chain {chain_id}: " f"{response['error']['message']}"
                    )
                    return None
            except CovalentAPIError as e:
                logger.error(f"API error for {address_info.address} on chain {chain_id}: {str(e)}")
                return None

        enriched_data = data.copy()
        enriched_data.update(
            {
                "wallet": {
                    "name": wallet.name,
                    "metadata": wallet.metadata,
                },
                "address": address_info.address,
                "chain_id": chain_id,
                "owner": address_info.owner,
                "purpose": address_info.purpose,
                "quote_currency": quote_currency,
            }
        )
        if data_type == DataType.BALANCE.value:
            self.balances.append(enriched_data)
        else:
            self.portfolios.append(enriched_data)
        return enriched_data

    async def _fetch_balance(
        self,
        wallet: Wallet,
        address_info: WalletAddress,
        chain_id: str,
        quote_currency: str,
    ) -> Optional[Dict[str, Any]]:
        """Fetch balance data and cache the result."""
        return await self._fetch_data(wallet, address_info, chain_id, quote_currency, DataType.BALANCE.value)

    async def _fetch_daily_portfolio(
        self,
        wallet: Wallet,
        address_info: WalletAddress,
        chain_id: str,
        quote_currency: str,
    ) -> Optional[Dict[str, Any]]:
        """Fetch daily portfolio data and cache the result."""
        return await self._fetch_data(wallet, address_info, chain_id, quote_currency, DataType.PORTFOLIO.value)

    async def fetch_all_balances(
        self, quote_currency: str
    ) -> List[Tuple[Union[Dict[str, Any], BaseException, None], Dict[str, Any]]]:
        """Fetch token balances asynchronously for all wallets."""
        tasks = [
            (
                self._fetch_balance(wallet, address_info, chain_id, quote_currency),
                {
                    "wallet_name": wallet.name,
                    "address": address_info.address,
                    "chain_id": chain_id,
                },
            )
            for wallet in self.wallets
            for address_info in wallet.addresses
            for chain_id in address_info.chain_ids
        ]
        results = await asyncio.gather(*(task[0] for task in tasks), return_exceptions=True)
        return list(zip(results, (task[1] for task in tasks)))

    async def fetch_daily_portfolio_balances(
        self, quote_currency: str
    ) -> List[Tuple[Union[Dict[str, Any], BaseException, None], Dict[str, Any]]]:
        """Fetch daily portfolio balances asynchronously for all wallets."""
        tasks = [
            (
                self._fetch_daily_portfolio(wallet, address_info, chain_id, quote_currency),
                {
                    "wallet_name": wallet.name,
                    "address": address_info.address,
                    "chain_id": chain_id,
                },
            )
            for wallet in self.wallets
            for address_info in wallet.addresses
            for chain_id in address_info.chain_ids
        ]
        results = await asyncio.gather(*(task[0] for task in tasks), return_exceptions=True)
        return list(zip(results, (task[1] for task in tasks)))

    def save_to_disk(self, data_list: List[Any], file_path: Path, compress: bool = False):
        """Save data to disk in JSON format, optionally compressed."""
        # Add timestamp to each item before saving
        for item in data_list:
            item["timestamp"] = time.time()

        if compress:
            file_path = file_path.with_suffix(".json.gz")
            with gzip.open(str(file_path), "wt", encoding="utf-8") as f:
                json.dump(data_list, f, indent=2)
        else:
            with file_path.open("w") as f:
                json.dump(data_list, f, indent=2)
        logger.info(f"Data saved to {file_path}")

    def load_from_disk(
        self, data_list: List[Any], cache: TTLCache[Tuple[str, str, str], Dict[str, Any]], file_path: Path
    ):
        """Load data from disk and update cache."""
        compressed_file_path = file_path.with_suffix(".json.gz")

        if compressed_file_path.is_file():
            file_path = compressed_file_path
            open_func = gzip.open  # type: ignore
            mode = "rt"
        elif file_path.is_file():
            open_func = open  # type: ignore
            mode = "r"
        else:
            logger.warning(f"Neither {file_path} nor {compressed_file_path} exist. Starting with empty data.")
            return

        try:
            with open_func(file_path, mode) as f:
                content = f.read().strip()
                if content:
                    loaded_data = json.loads(content)
                    if isinstance(loaded_data, list):
                        data_list.clear()
                        data_list.extend(loaded_data)
                        logger.info(f"Data loaded from {file_path}")
                        # Update cache with loaded data, respecting TTL
                        current_time = time.time()
                        for item in loaded_data:
                            if isinstance(item, dict):
                                address = item.get("address")
                                chain_id = item.get("chain_id")
                                quote_currency = item.get("quote_currency")
                                if address and chain_id and quote_currency:
                                    cache_key = (address, chain_id, quote_currency)
                                    # Only add to cache if the data is not expired
                                    if current_time - item.get("timestamp", 0) < self.cache_ttl:
                                        cache[cache_key] = item
                                    else:
                                        logger.debug(f"Skipping expired cache item: {cache_key}")
                                else:
                                    logger.warning(f"Skipping invalid item: {item}")
                            else:
                                logger.warning(f"Skipping non-dict item: {item}")
                    else:
                        logger.error(f"Expected a list in {file_path}, but got {type(loaded_data)}")
                else:
                    logger.warning(f"File {file_path} is empty. Starting with empty data.")
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON from {file_path}: {str(e)}. Starting with empty data.")

    def save_balances_to_disk(self, file_path: Path, compress: bool = False):
        """Save balances to disk in JSON format, optionally compressed."""
        self.save_to_disk(self.balances, file_path, compress)

    def load_balances_from_disk(self, file_path: Path):
        """Load balances from disk."""
        self.load_from_disk(self.balances, self.balances_cache, file_path)

    def save_portfolios_to_disk(self, file_path: Path, compress: bool = False):
        """Save portfolio data to disk in JSON format, optionally compressed."""
        self.save_to_disk(self.portfolios, file_path, compress)

    def load_portfolios_from_disk(self, file_path: Path):
        """Load portfolio data from disk."""
        self.load_from_disk(self.portfolios, self.portfolios_cache, file_path)
