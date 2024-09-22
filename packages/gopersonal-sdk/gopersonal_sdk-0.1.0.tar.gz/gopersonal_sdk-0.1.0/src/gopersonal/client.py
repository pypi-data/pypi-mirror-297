from .api import GoPersonalAPI

class GoPersonal:
    def __init__(self):
        self._api = GoPersonalAPI()

    async def init(self, config=None):
        return await self._api.init(config)

    async def bulk_search(self, terms):
        return await self._api.bulk_search(terms)