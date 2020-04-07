from strategies.second.second import Second
from lib.data_loader import load_candlesticks
from lib.backtest import Backtest
from lib.charting import chartTrades


def main():
    candlesticks = load_candlesticks("1h")
    shorter_candlesticks = load_candlesticks("1m")

    trade_start_position = 18000
    trade_end_position = len(candlesticks)
    features = Second.generate_features(candlesticks)
    targets = Second._generate_target(features)

    features.to_csv("strategies/second/tmp/features.csv")

    signals = Backtest.run(
        TradingStrategy=Second,
        features=features,
        candlesticks=candlesticks,
        shorter_candlesticks=shorter_candlesticks,
        start_position=trade_start_position,
        end_position=trade_end_position,
    )
    # signals = Backtest._runWithTarget(Second, features, targets ,candlesticks, trade_start_position, trade_end_position)
    signals.to_csv("strategies/second/tmp/signals.csv")

    trades = Backtest.evaluate(signals, candlesticks, trade_start_position, trade_end_position)
    trades.to_csv("strategies/second/tmp/trades.csv")

    chartTrades(
        trades,
        candlesticks,
        trade_start_position,
        trade_end_position,
        "strategies/second/tmp/chart.html",
    )


if __name__ == "__main__":
    main()
