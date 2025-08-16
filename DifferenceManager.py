from decimal import Decimal, getcontext

getcontext().prec = 28


class DifferenceManager:
    def __init__(self, lists):
        self.lists = lists
        if not hasattr(self, 'tokenDict'):
            self.tokenDict = {}

    def sort_pairs(self):
        for sublist in self.lists:
            exchange = sublist[0]
            for item in sublist[1:]:
                token = item['token']
                price = float(item['price'])
                if token not in self.tokenDict:
                    self.tokenDict[token] = {'notification': False}
                self.tokenDict[token][exchange] = price

    def calculate_difference(self):
        for token, markets in self.tokenDict.items():
            exchanges = {k: v for k, v in markets.items() if k not in ['difference', 'notification']}
            if len(exchanges) < 2:
                continue

            diff = {}
            keys = list(exchanges.keys())
            for i in range(len(keys)):
                for j in range(i + 1, len(keys)):
                    k1, k2 = keys[i], keys[j]
                    price1 = Decimal(str(exchanges[k1]))
                    price2 = Decimal(str(exchanges[k2]))

                    if price1 == 0 or price2 == 0:
                        continue

                    percent_diff = abs(price1 - price2) / ((price1 + price2) / 2) * Decimal('100')
                    diff[f"{k1}{k2}"] = float(percent_diff)

            if diff:
                self.tokenDict[token]['difference'] = diff

    def get_results(self):
        results = {}
        notifications_to_send = []

        for token, data in self.tokenDict.items():
            if 'difference' in data and data['difference']:

                sorted_diffs = sorted(data['difference'].items(), key=lambda x: abs(x[1]), reverse=True)

                if sorted_diffs:
                    top_diff_pair, top_diff_value = sorted_diffs[0]
                    current_notification_status = self.tokenDict[token]['notification']

                    if top_diff_value > 6.8 and not current_notification_status:
                        self.tokenDict[token]['notification'] = True
                        notifications_to_send.append(
                            f"Сповіщення: пара {token} - {top_diff_pair} тепер актуальна! Різниця > 7.0% ({top_diff_value:.2f}%)")

                    elif top_diff_value < 3.0 and current_notification_status:
                        self.tokenDict[token]['notification'] = False
                        notifications_to_send.append(
                            f"Сповіщення: пара {token} - {top_diff_pair} більше не актуальна. Різниця < 3.0% ({top_diff_value:.2f}%)")

                    if top_diff_value > 6.8:
                        results[token] = {
                            'notification': self.tokenDict[token]['notification'],
                            'difference': {pair: diff for pair, diff in sorted_diffs if diff > 6.8}
                        }

        return results, notifications_to_send