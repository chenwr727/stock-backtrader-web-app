import backtrader as bt

from .base import BaseStrategy


class MaCrossStrategy(BaseStrategy):
    """MaCross strategy - 双均线交叉策略"""

    _name = "MaCross"
    params = (("printlog", False), ("fast_length", 10), ("slow_length", 50))

    def __init__(self) -> None:
        super().__init__()
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close

        # To keep track of pending orders and buy price/commission
        self.order = None
        self.buyprice = None
        self.buycomm = None

        # Add a MovingAverageSimple indicator
        ma_fast = bt.ind.SMA(period=self.params.fast_length)
        ma_slow = bt.ind.SMA(period=self.params.slow_length)

        self.crossover = bt.ind.CrossOver(ma_fast, ma_slow)

    def next(self) -> None:
        # Simply log the closing price of the series from the reference
        self.log(f"Close, {self.dataclose[0]:.2f}")

        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return

        # Check if we are in the market
        if not self.position:
            # Not yet ... we MIGHT BUY if ...
            if self.crossover > 0:
                # BUY, BUY, BUY!!! (with all possible default parameters)
                self.log(f"BUY CREATE, {self.dataclose[0]:.2f}")
                # Keep track of the created order to avoid a 2nd order
                self.order = self.buy()
        else:
            if self.crossover < 0:
                # SELL, SELL, SELL!!! (with all possible default parameters)
                self.log(f"SELL CREATE, {self.dataclose[0]:.2f}")
                # Keep track of the created order to avoid a 2nd order
                self.order = self.sell()
