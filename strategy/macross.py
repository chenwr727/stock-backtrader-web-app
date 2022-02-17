import backtrader as bt


class MaCrossStrategy(bt.Strategy):

    params = (("fast_length", 10), ("slow_length", 50))

    def __init__(self):
        ma_fast = bt.ind.SMA(period=self.params.fast_length)
        ma_slow = bt.ind.SMA(period=self.params.slow_length)

        self.crossover = bt.ind.CrossOver(ma_fast, ma_slow)

    def next(self):
        if not self.position:
            if self.crossover > 0:
                self.buy()
        elif self.crossover < 0:
            self.close()
