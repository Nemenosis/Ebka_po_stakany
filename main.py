import asyncio

from DifferenceManager import DifferenceManager
from controllers.controllers import GateAPIController, MexcAPIController, OurbitAPIController
import time


async def main():
    while True:
        start = time.perf_counter()
        gate = GateAPIController("https://www.gate.com/apiw/v2/futures/usdt/tickers", "Gate")
        mexc = MexcAPIController("https://futures.mexc.com/api/v1/contract/ticker", "Mexc")
        ourbit = OurbitAPIController("https://futures.ourbit.com/api/v1/contract/ticker", "Ourbit")
        await asyncio.gather(gate.fetch(), mexc.fetch(), ourbit.fetch())
        results = await asyncio.gather(gate.prepare_list(),
                                       mexc.prepare_list(),
                                       ourbit.prepare_list())
        diff_manager = DifferenceManager(results)
        diff_manager.sort_pairs()
        diff_manager.calculate_difference()
        print(diff_manager.get_results())
        end = time.perf_counter()
        print(f"Время выполнения: {end - start:.6f} секунд")


asyncio.run(main())
