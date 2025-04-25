from typing import Optional

import backtrader as bt

from utils.logs import logger


class BaseStrategy(bt.Strategy):
    """base strategy"""

    _name = "base"
    params = (("printlog", False),)

    def log(self, txt: str, dt: Optional[bt.datetime.date] = None, doprint: bool = False) -> None:
        """Logging function for this strategy"""
        if self.params.printlog or doprint:
            dt = dt or self.datas[0].datetime.date(0)
            logger.info("%s, %s" % (dt.isoformat(), txt))

    def notify_order(self, order: bt.OrderBase) -> None:
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    "BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f"
                    % (order.executed.price, order.executed.value, order.executed.comm)
                )

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:  # Sell
                self.log(
                    "SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f"
                    % (order.executed.price, order.executed.value, order.executed.comm)
                )

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log("Order Canceled/Margin/Rejected")

        # Write down: no pending order
        self.order = None

    def notify_trade(self, trade: bt.Trade) -> None:
        if not trade.isclosed:
            return

        self.log("OPERATION PROFIT, GROSS %.2f, NET %.2f" % (trade.pnl, trade.pnlcomm))

    def next(self) -> None:
        pass

    def stop(self) -> None:
        params = [f"{k}_{v}" for k, v in self.params._getkwargs().items() if k != "printlog"]
        self.log(
            "(%s %s) Ending Value %.2f" % (self._name, " ".join(params), self.broker.getvalue()),
            doprint=True,
        )
