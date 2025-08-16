import asyncio
import time
from loguru import logger
from DifferenceManager import DifferenceManager
from TelegramBot import TelegramBot
from controllers.controllers import GateAPIController, MexcAPIController, OurbitAPIController
from collections import deque

TELEGRAM_BOT_TOKEN = "8421137605:AAECvTERMBzB_TOJb8vDoqU0YL0AcTqGMB8"


async def main():
    bot = TelegramBot(TELEGRAM_BOT_TOKEN)
    diff_manager = DifferenceManager([])

    gate = GateAPIController("https://www.gate.com/apiw/v2/futures/usdt/tickers", "Gate")
    mexc = MexcAPIController("https://futures.mexc.com/api/v1/contract/ticker", "Mexc")
    ourbit = OurbitAPIController("https://futures.ourbit.com/api/v1/contract/ticker", "Ourbit")
    asyncio.create_task(bot.start_polling())

    while True:
        start = time.perf_counter()
        await asyncio.gather(gate.fetch(), mexc.fetch(), ourbit.fetch())
        results_data = await asyncio.gather(gate.prepare_list(),
                                            mexc.prepare_list(),
                                            ourbit.prepare_list())

        diff_manager.lists = results_data
        diff_manager.sort_pairs()
        diff_manager.calculate_difference()

        results, notifications_to_send = diff_manager.get_results()

        if notifications_to_send:
            for user_id in bot.user_ids:
                for message in notifications_to_send:
                    await bot.send_message(user_id, message)

        logger.info(results)
        end = time.perf_counter()
        logger.info(f"Час виконання: {end - start:.6f} секунд")


asyncio.run(main())
