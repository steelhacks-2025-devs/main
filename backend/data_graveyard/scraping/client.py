import asyncio
import json
import aiohttp
from typing import Optional
# from config import load_config

class WPRDC_Client:
    BASE_URL = "https://tools.wprdc.org/property-api/v0/parcels/"
    """
    Base client for sending requests to the API.
    """
    def __init__(self, max_requests: int = 50):
        self.cookies, self.headers, self.endpoints = None, None, None
        self._session: Optional[aiohttp.ClientSession] = None
        self.semaphore = asyncio.Semaphore(max_requests)

    async def __aenter__(self):
        """Async context manager entry"""
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        """Async context manager exit"""
        await self.close()


    async def connect(self):
        """Create client session if it doesn't exist"""
        if self._session is None:
            self._session = aiohttp.ClientSession()

    async def close(self):
        """Close client session if it exists"""
        if self._session:
            await self._session.close()
            self._session = None
    
    async def _make_request(self, path: str, params:dict) -> dict:
        """Make a request to the API"""
        endpoint_path_url = f"{self.BASE_URL}{path}"
        async with self.semaphore:
            async with self._session.get(
                endpoint_path_url,
                # cookies=self.cookies,
                # headers=self.headers,
                params=params
            ) as resp:
                print(f"Querying URL: {resp.url}")
                try:
                    resp.raise_for_status()
                    response = await resp.json()
                    if response["success"]:
                        return response
                    raise RuntimeError("API request unsuccessful")
                except aiohttp.ClientResponseError as e:
                    raise e
                except json.JSONDecodeError as e:
                    raise e
