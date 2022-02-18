from strategy import MaStrategy

from .base_test import StrategyTest, run_back_trader


class MaStrategyTest(StrategyTest):
    """ma strategy test"""

    def test_ma(self):
        self.result = run_back_trader(self.cerebro, MaStrategy, maperiod=range(3, 31))
