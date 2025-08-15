import aiohttp
from loguru import logger


class BrokerAPIController:
    def __init__(self, url):
        self.url = url
        self.list = None

    async def fetch(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url) as response:
                if response.status == 200:
                    self.list = await response.json()
                else:
                    logger.info("Error", response.status)
                    return None

    def get_final_list(self, symbol, price):
        result = []
        for item in self.list:
            result.append({
                "token": item[symbol].split("_")[0],
                "price": item[price]
            })

        return result
