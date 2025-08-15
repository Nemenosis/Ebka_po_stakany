from .BrokerAPIController import BrokerAPIController


class GateAPIController(BrokerAPIController):
    def __init__(self, url):
        super().__init__(url)

    async def prepare_list(self):
        self.list = self.list['data']
        return self.get_final_list("contract", "last")


class MexcAPIController(BrokerAPIController):
    def __init__(self, url):
        super().__init__(url)

    async def prepare_list(self):
        self.list = self.list['data']
        return self.get_final_list("symbol", "lastPrice")


class OurbitAPIController(BrokerAPIController):
    def __init__(self, url):
        super().__init__(url)

    async def prepare_list(self):
        self.list = self.list['data']
        return self.get_final_list("symbol", "lastPrice")

