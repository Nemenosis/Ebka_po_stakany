import time
import asyncio
from controllers.controllers import GateAPIController, MexcAPIController, OurbitAPIController


async def token_listener(token, symbol_deque, instances):
    if not token in symbol_deque:
        symbol_deque.appendLeft(token)
        await buffer_process(token, symbol_deque, instances)


async def buffer_process(token_data, dequeue, instances, delay=30):
    start = time.monotonic()
    token_name, token_info = list(token_data.items())[0]
    exchanges = [key for key in token_info.keys() if key not in ('notification', 'difference')]
    print("Биржи:", exchanges)

    while time.monotonic() - start < delay:
        diff = {}
        for i in range(len(exchanges)):
            for j in range(i + 1, len(exchanges)):
                e1, e2 = exchanges[i], exchanges[j]
                p1 = await instances[e1.lower()].get_ticker(token_name)
                p2 = await instances[e2.lower()].get_ticker(token_name)

                percent_diff = abs(p1 - p2) / ((p1 + p2) / 2) * 100
                diff[f"{e1}-{e2}"] = percent_diff
                print(f"Разница {e1}-{e2} = {percent_diff:.2f}%")

                if percent_diff < 6.5:
                    print("Меньше 6.5% → стоп")
                    dequeue.pop()
                    return

        print("Текущий токен:", token_name)
        await asyncio.sleep(1)


gate = GateAPIController()
mexc = MexcAPIController()


async def test():
    print(await gate.get_ticker("BTC_USDT"))


#asyncio.run(buffer_process({'BOOM': {'notification': False, 'Gate': 0.01334, 'Mexc': 0.0153,
#                                    'difference': {'GateMexc': 1.4142165984369186}}}))
asyncio.run(test())
