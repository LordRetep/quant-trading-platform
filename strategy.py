import backtrader as bt
import numpy as np
from collections import deque

class StatArbStrategy(bt.Strategy):
    params = dict(
        lookback=20,  # Lookback period for mean and std
        z_entry=2.0,  # Z-score threshold for entry
        z_exit=0.5,   # Z-score threshold for exit
        size=1000,    # Position size per asset
    )

    def __init__(self):
        self.pairs = []
        self.spreads = {}
        self.z_scores = {}
        self.positions = {}

        # Form pairs from datas (assume even number or skip last if odd)
        for i in range(0, len(self.datas), 2):
            if i + 1 < len(self.datas):  # Ensure we have a pair
                pair = (self.datas[i], self.datas[i + 1])
                self.pairs.append(pair)
                pair_key = f"{pair[0]._name}_{pair[1]._name}"
                self.spreads[pair_key] = deque(maxlen=self.p.lookback)
                self.z_scores[pair_key] = deque(maxlen=self.p.lookback)
                self.positions[pair[0]._name] = 0
                self.positions[pair[1]._name] = 0

    def next(self):
        for pair in self.pairs:
            asset1, asset2 = pair
            pair_key = f"{asset1._name}_{asset2._name}"

            if len(asset1) < self.p.lookback:  # Wait for enough data
                continue

            # Calculate spread (close price difference)
            spread = asset1.close[0] - asset2.close[0]
            self.spreads[pair_key].append(spread)

            # Compute z-score
            if len(self.spreads[pair_key]) == self.p.lookback:
                mean = np.mean(self.spreads[pair_key])
                std = np.std(self.spreads[pair_key])
                if std == 0:  # Avoid division by zero
                    continue
                z_score = (spread - mean) / std
                self.z_scores[pair_key].append(z_score)

                # Trading logic
                # Long spread: Buy asset1, Sell asset2
                if z_score < -self.p.z_entry and not self.positions[asset1._name]:
                    self.buy(data=asset1, size=self.p.size)
                    self.sell(data=asset2, size=self.p.size)
                    self.positions[asset1._name] = self.p.size
                    self.positions[asset2._name] = -self.p.size

                # Short spread: Sell asset1, Buy asset2
                elif z_score > self.p.z_entry and not self.positions[asset1._name]:
                    self.sell(data=asset1, size=self.p.size)
                    self.buy(data=asset2, size=self.p.size)
                    self.positions[asset1._name] = -self.p.size
                    self.positions[asset2._name] = self.p.size

                # Exit positions when z-score reverts
                elif abs(z_score) < self.p.z_exit and self.positions[asset1._name]:
                    if self.positions[asset1._name] > 0:
                        self.sell(data=asset1, size=self.p.size)
                        self.buy(data=asset2, size=self.p.size)
                    else:
                        self.buy(data=asset1, size=self.p.size)
                        self.sell(data=asset2, size=self.p.size)
                    self.positions[asset1._name] = 0
                    self.positions[asset2._name] = 0