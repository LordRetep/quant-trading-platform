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
            if data.close[0] <= 0:  # Avoid division by zero
                continue

            if name not in self.last_price:
                self.last_price[name] = data.close[0]
                continue

            change = (data.close[0] - self.last_price[name]) / self.last_price[name]

            size = self.p.stake / data.close[0]
            if size <= 0:  # Ensure valid size
                continue

            if change <= -0.02:  # Buy on 2% drop
                reward_ratio = 5 if random.random() < 0.2 else 1
                stop_loss = data.close[0] * (1 - self.p.risk_pct)
                take_profit = data.close[0] * (1 + self.p.risk_pct * reward_ratio)

                self.buy(data=data,
                         size=size,
                         exectype=bt.Order.Market,
                         price=data.close[0],
                         stopprice=stop_loss,
                         valid=None)

            elif change >= 0.02:  # Sell on 2% rise
                reward_ratio = 5 if random.random() < 0.2 else 1
                stop_loss = data.close[0] * (1 + self.p.risk_pct)
                take_profit = data.close[0] * (1 - self.p.risk_pct * reward_ratio)

                self.sell(data=data,
                          size=size,
                          exectype=bt.Order.Market,
                          price=data.close[0],
                          stopprice=stop_loss,
                          valid=None)

            self.last_price[name] = data.close[0]