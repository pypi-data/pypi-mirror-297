# api_clients.py
import asyncio
import json
import logging
import os
from typing import Any, Dict, Optional

import aiohttp
from dotenv import load_dotenv

# Create a logger for this module
logger = logging.getLogger(__name__)


class CovalentAPIError(Exception):
    """Custom exception for Covalent API errors."""


class AsyncAPIClientBase:
    """Base class for asynchronous API clients."""

    def __init__(self, api_key: str):
        self.api_key = api_key
        logger.debug(f"Initialized AsyncAPIClientBase with API key: {api_key[:5]}...")

    async def fetch(
        self,
        session: aiohttp.ClientSession,
        url: str,
        method: str = "GET",
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
    ) -> aiohttp.ClientResponse:
        headers = {"Authorization": f"Bearer {self.api_key}"}
        logger.debug(f"Sending {method} request to {url}")
        response = await session.request(method, url, headers=headers, params=params, json=data)
        logger.debug(f"Received response with status code: {response.status}")
        return response

    @staticmethod
    async def _process_response(response: aiohttp.ClientResponse) -> Dict[str, Any]:
        result: Dict[str, Any] = {
            "success": response.status >= 200 and response.status < 400,
            "status_code": response.status,
            "reason": response.reason,
            "data": None,
            "error": None,
        }

        try:
            json_data = await response.json()
            logger.debug("Successfully parsed JSON response")
        except (aiohttp.ContentTypeError, ValueError):
            json_data = None
            logger.warning("Failed to parse JSON response")

        if result["success"]:
            result["data"] = json_data or await response.text()
            logger.info(f"Successful API response: {result['status_code']}")
        else:
            error_message = None
            error_code = None

            if json_data:
                error_message = json_data.get("error") or json_data.get("message")
                error_code = json_data.get("code") or json_data.get("error_code")
            else:
                error_message = await response.text()

            result["error"] = {"message": error_message, "code": error_code}
            logger.error(f"API error: {result['status_code']}, {error_message}")

        await response.close()  # type: ignore
        return result


class AsyncCovalentClient(AsyncAPIClientBase):
    """Asynchronously fetches data using the Covalent API."""

    BASE_URL = "https://api.covalenthq.com/v1"

    async def get_token_balances(self, chain_id: str, address: str, quote_currency: str) -> Dict[str, Any]:
        url = f"{self.BASE_URL}/{chain_id}/address/{address}/balances_v2/?quote-currency={quote_currency}"
        logger.info(f"Fetching token balances for address {address} on chain {chain_id}")
        async with aiohttp.ClientSession() as session:
            response = await self.fetch(session, url)
            result = await self._process_response(response)
            if not result["success"]:
                logger.error(f"Failed to fetch token balances: {result['error']['message']}")
                raise CovalentAPIError(f"API error: {result['status_code']}, {result['error']['message']}")
            if isinstance(result["data"], dict) and "data" in result["data"]:
                result["data"] = result["data"]["data"]
            logger.info(f"Successfully fetched token balances for address {address}")
            return result

    async def get_daily_portfolio_balances(
        self, chain_id: str, address: str, quote_currency: str, days: int
    ) -> Dict[str, Any]:
        url = f"{self.BASE_URL}/{chain_id}/address/{address}/portfolio_v2/?quote-currency={quote_currency}&days={days}"
        logger.info(f"Fetching daily portfolio balances for address {address} on chain {chain_id}")
        async with aiohttp.ClientSession() as session:
            response = await self.fetch(session, url)
            result = await self._process_response(response)
            if not result["success"]:
                logger.error(f"Failed to fetch daily portfolio balances: {result['error']['message']}")
                raise CovalentAPIError(f"API error: {result['status_code']}, {result['error']['message']}")
            if isinstance(result["data"], dict) and "data" in result["data"]:
                result["data"] = result["data"]["data"]
            logger.info(f"Successfully fetched daily portfolio balances for address {address}")
            return result


class AsyncGenericAPIClient(AsyncAPIClientBase):
    """A template for asynchronous API clients."""

    BASE_URL = "https://api.example.com/v1"  # Replace with actual API base URL

    async def get_resource(self, resource_id: str) -> Dict[str, Any]:
        url = f"{self.BASE_URL}/resources/{resource_id}"
        logger.info(f"Fetching resource with ID {resource_id}")
        async with aiohttp.ClientSession() as session:
            response = await self.fetch(session, url)
            result = await self._process_response(response)
            if not result["success"]:
                logger.error(f"Failed to fetch resource: {result['error']['message']}")
                raise Exception(f"API error: {result['status_code']}, {result['error']['message']}")
            logger.info(f"Successfully fetched resource with ID {resource_id}")
            return result

    async def create_resource(self, resource_data: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.BASE_URL}/resources"
        logger.info("Creating new resource")
        async with aiohttp.ClientSession() as session:
            response = await self.fetch(session, url, method="POST", data=resource_data)
            result = await self._process_response(response)
            if not result["success"]:
                logger.error(f"Failed to create resource: {result['error']['message']}")
                raise Exception(f"API error: {result['status_code']}, {result['error']['message']}")
            logger.info("Successfully created new resource")
            return result


if __name__ == "__main__":
    load_dotenv()
    api_key = os.getenv("COVALENT_API_KEY")

    if not api_key:
        logger.error("COVALENT_API_KEY not found in environment variables.")
        exit(1)

    fetcher = AsyncCovalentClient(api_key)

    chain_id = "1"  # Ethereum mainnet
    address = "0x742d35Cc6634C0532925a3b844Bc454e4438f44e"  # Example address
    quote_currency = "USD"

    async def main():
        try:
            result = await fetcher.get_daily_portfolio_balances(chain_id, address, quote_currency, days=7)
            logger.info("Portfolio balances:")
            logger.info(json.dumps(result, indent=2)[:2000])  # Print first 2000 characters (roughly 50 lines)
        except CovalentAPIError as e:
            logger.error(f"Error fetching portfolio balances: {e}")

    asyncio.run(main())
