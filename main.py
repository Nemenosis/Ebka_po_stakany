import asyncio
from controllers.controllers import GateAPIController, MexcAPIController, OurbitAPIController
import time


async def main():
    start = time.perf_counter()
    gate = GateAPIController("https://www.gate.com/apiw/v2/futures/usdt/tickers")
    mexc = MexcAPIController("https://futures.mexc.com/api/v1/contract/ticker")
    ourbit = OurbitAPIController("https://futures.ourbit.com/api/v1/contract/ticker")
    await asyncio.gather(gate.fetch(), mexc.fetch(), ourbit.fetch())
    results = await asyncio.gather(gate.prepare_list(),
                                   mexc.prepare_list(),
                                   ourbit.prepare_list())
    print(results)
    end = time.perf_counter()
    print(f"Время выполнения: {end - start:.6f} секунд")


asyncio.run(main())
