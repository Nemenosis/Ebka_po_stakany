import aiohttp
from loguru import logger


class BrokerAPIController:
    def __init__(self, url, broker):
        self.url = url
        self.list = None
        self.broker = broker

    async def fetch(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url) as response:
                if response.status == 200:
                    self.list = await response.json()
                else:
                    logger.info("Error", response.status)
                    return None

    def get_final_list(self, symbol: str, price: str) -> list:
        return [
            {
                "token": item[symbol].split("_")[0],
                "price": item[price],
                "exchange": self.broker
            }
            for item in self.list
            if item[symbol].endswith("_USDT") and "TRUMP" not in item[symbol].upper()
        ]
