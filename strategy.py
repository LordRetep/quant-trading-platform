import backtrader as bt
import random

class TwoPercentRuleStrategy(bt.Strategy):
    params = dict(
        stake=10000,
        risk_pct=0.02,
    )

    def __init__(self):
        self.last_price = {}

    def next(self):
        for data in self.datas:
            name = data._name
            if name not in self.last_price:
                self.last_price[name] = data.close[0]
                continue

            change = (data.close[0] - self.last_price[name]) / self.last_price[name]

            if change <= -0.02:
                reward_ratio = 5 if random.random() < 0.2 else 1
                stop_loss = data.close[0] * self.p.risk_pct
                take_profit = stop_loss * reward_ratio

                self.buy(data=data,
                         size=self.p.stake / data.close[0],
                         exectype=bt.Order.Market)

            elif change >= 0.02:
                reward_ratio = 5 if random.random() < 0.2 else 1
                stop_loss = data.close[0] * self.p.risk_pct
                take_profit = stop_loss * reward_ratio

                self.sell(data=data,
                          size=self.p.stake / data.close[0],
                          exectype=bt.Order.Market)

            self.last_price[name] = data.close[0]
