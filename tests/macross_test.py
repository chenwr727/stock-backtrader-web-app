from strategy import MaCrossStrategy

from .base_test import StrategyTest, run_back_trader


class MaCrossStrategyTest(StrategyTest):
    """ma cross strategy test"""

    def test_ma(self):
        self.result = run_back_trader(
            self.cerebro,
            MaCrossStrategy,
            fast_length=range(1, 11, 5),
            slow_length=range(25, 35, 5),
        )
