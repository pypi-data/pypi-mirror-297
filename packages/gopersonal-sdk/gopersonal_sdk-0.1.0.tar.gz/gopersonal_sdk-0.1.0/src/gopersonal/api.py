import os
import aiohttp
from typing import Dict, List, Optional

class GoPersonalAPI:
    def __init__(self):
        self.client_id = None
        self.client_secret = None
        self.region = None
        self.endpoint = None
        self.token = None

    async def init(self, config: Optional[Dict[str, str]] = None) -> Dict[str, str]:
        if config is None:
            config = {}
        
        self.client_id = config.get('client_id') or os.environ.get('GO_PERSONAL_CLIENT_ID')
        self.client_secret = config.get('client_secret') or os.environ.get('GO_PERSONAL_CLIENT_SECRET')
        self.region = config.get('region', 'BR')

        if not self.client_id or not self.client_secret:
            raise ValueError("Client ID and Client Secret must be provided either in config or as environment variables.")

        self.endpoint = {
            'BR': 'https://discover.gopersonal.ai',
            'D': 'https://go-discover-dev.goshops.ai'
        }.get(self.region)

        if not self.endpoint:
            raise ValueError(f"Invalid region: {self.region}")

        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.endpoint}/channel/init",
                json={
                    "clientId": self.client_id,
                    "clientSecret": self.client_secret
                }
            ) as response:
                response.raise_for_status()
                data = await response.json()
                self.token = data.get('token')
                return {"token": self.token}

    async def bulk_search(self, terms: List[str]) -> Dict:
        if not self.token:
            raise ValueError("API not initialized. Call init() first.")

        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.endpoint}/item/bulk-search",
                headers={"Authorization": f"Bearer {self.token}"},
                json={"terms": terms}
            ) as response:
                response.raise_for_status()
                return await response.json()