import backtrader as bt

from .base import BaseStrategy


class MaStrategy(BaseStrategy):
    """Ma strategy"""

    _name = "Ma"
    params = (
        ("maperiod", 15),
        ("printlog", False),
    )

    def __init__(self) -> None:
        super().__init__()
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close

        # To keep track of pending orders and buy price/commission
        self.order = None
        self.buyprice = None
        self.buycomm = None

        # Add a MovingAverageSimple indicator
        self.sma = bt.indicators.SMA(self.datas[0], period=self.params.maperiod)

    def next(self) -> None:
        # Simply log the closing price of the series from the reference
        self.log(f"Close, {self.dataclose[0]:.2f}")

        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return

        # Check if we are in the market
        if not self.position:
            # Not yet ... we MIGHT BUY if ...
            if self.dataclose[0] > self.sma[0]:
                # BUY, BUY, BUY!!! (with all possible default parameters)
                self.log(f"BUY CREATE, {self.dataclose[0]:.2f}")
                # Keep track of the created order to avoid a 2nd order
                self.order = self.buy()
        else:
            if self.dataclose[0] < self.sma[0]:
                # SELL, SELL, SELL!!! (with all possible default parameters)
                self.log(f"SELL CREATE, {self.dataclose[0]:.2f}")
                # Keep track of the created order to avoid a 2nd order
                self.order = self.sell()
