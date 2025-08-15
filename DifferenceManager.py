class DifferenceManager:
    def __init__(self, lists):
        self.lists = lists
        self.tokenDict = {}

    def sort_pairs(self):
        for sublist in self.lists:
            exchange = sublist[0]
            for item in sublist[1:]:
                token = item['token']
                price = float(item['price'])
                if token not in self.tokenDict:
                    self.tokenDict[token] = {}
                self.tokenDict[token][exchange] = price

    def calculate_difference(self):
        for token, markets in self.tokenDict.items():
            diff = {}
            keys = list(markets.keys())
            for i in range(len(keys)):
                for j in range(i + 1, len(keys)):
                    k1, k2 = keys[i], keys[j]
                    percent_diff = abs(markets[k1] - markets[k2]) / markets[k1] * 100
                    diff[f"{k1}{k2}"] = percent_diff
            self.tokenDict[token]['difference'] = diff

        tokens_to_remove = [token for token, data in self.tokenDict.items() if not data.get('difference')]
        for token in tokens_to_remove:
            del self.tokenDict[token]

    def get_results(self):
        results = {}

        for token, data in self.tokenDict.items():

            if 'difference' not in data or not data['difference']:
                continue

            filtered_diff = {pair: diff for pair, diff in sorted(
                data['difference'].items(), key=lambda x: abs(x[1]), reverse=True
            ) if abs(diff) > 3.0}

            if filtered_diff:
                results[token] = {
                    **data,
                    'difference': filtered_diff
                }

        return results
