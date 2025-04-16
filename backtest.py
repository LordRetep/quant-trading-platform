import backtrader as bt
import pandas as pd
from datetime import datetime
from strategy import TwoPercentRuleStrategy
from data_loader import get_data
import matplotlib.pyplot as plt

def run_backtest(assets, start_date, end_date):
    cerebro = bt.Cerebro()
    cerebro.addstrategy(TwoPercentRuleStrategy)
    cerebro.broker.set_cash(100000)

    for asset in assets:
        df = get_data(asset, start_date, end_date)
        if df.empty:
            continue  # Skip if no data
        data = bt.feeds.PandasData(dataname=df, name=asset)
        cerebro.adddata(data)

    cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpe')
    cerebro.addanalyzer(bt.analyzers.DrawDown, _name='drawdown')
    cerebro.addanalyzer(bt.analyzers.Returns, _name='returns')

    result = cerebro.run()
    if not result:
        raise ValueError("Backtest failed to produce results")

    strat = result[0]

    # Extract total return as a percentage
    returns_analysis = strat.analyzers.returns.get_analysis()
    total_return_pct = returns_analysis.get('rtot', 0.0) * 100  # Convert decimal to %

    stats = {
        "Sharpe Ratio": strat.analyzers.sharpe.get_analysis(),
        "Max Drawdown": strat.analyzers.drawdown.get_analysis(),
        "Total Return (%)": round(total_return_pct, 2),  # Round to 2 decimal places
        "Returns Analysis": returns_analysis  # Keep full analysis for other metrics
    }

    fig = cerebro.plot(style='candlestick', iplot=False)[0][0]
    return stats, fig