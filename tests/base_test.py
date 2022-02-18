import unittest
from datetime import datetime

import akshare as ak
import backtrader as bt
import backtrader.analyzers as btanalyzers
import pandas as pd
from strategy.base import BaseStrategy
from utils.processing import load_strategys


class StrategyTest(unittest.TestCase):
    """strategy test"""

    def setUp(self):
        stock_hfq_df = ak.stock_zh_a_hist(
            symbol="600070", adjust="hfq", start_date="20000101", end_date="20210617"
        ).iloc[:, :6]
        stock_hfq_df.columns = [
            "date",
            "open",
            "close",
            "high",
            "low",
            "volume",
        ]
        stock_hfq_df.index = pd.to_datetime(stock_hfq_df["date"])
        start_date = datetime(1991, 4, 3)
        end_date = datetime(2021, 6, 16)
        data = bt.feeds.PandasData(
            dataname=stock_hfq_df, fromdate=start_date, todate=end_date
        )

        self.cerebro = cerebro = bt.Cerebro()
        cerebro.adddata(data)
        cerebro.broker.setcash(1000000)
        cerebro.broker.setcommission(commission=0.001)
        cerebro.addsizer(bt.sizers.FixedSize, stake=100)
        cerebro.addanalyzer(btanalyzers.SharpeRatio, _name="sharpe")
        cerebro.addanalyzer(btanalyzers.DrawDown, _name="drawdown")
        cerebro.addanalyzer(btanalyzers.Returns, _name="returns")

        self.strategys = load_strategys("./config/strategy.yaml")
        self.result = None

    def tearDown(self):
        self.assertIsInstance(self.result, pd.DataFrame)
        print(self.result)


def run_back_trader(
    cerebro: bt.Cerebro, strategy: BaseStrategy, **kwargs
) -> pd.DataFrame:
    """run back trader

    Args:
        cerebro (bt.Cerebro): cerebro
        strategy (BaseStrategy): strategy

    Returns:
        pd.DataFrame: result
    """
    cerebro.optstrategy(strategy, **kwargs)
    back = cerebro.run()
    par_list = []
    for x in back:
        par = []
        for param in kwargs.keys():
            par.append(x[0].params._getkwargs()[param])
        par.extend(
            [
                x[0].analyzers.returns.get_analysis()["rnorm100"],
                x[0].analyzers.drawdown.get_analysis()["max"]["drawdown"],
                x[0].analyzers.sharpe.get_analysis()["sharperatio"],
            ]
        )
        par_list.append(par)
    columns = list(kwargs.keys())
    columns.extend(["return", "dd", "sharpe"])
    par_df = pd.DataFrame(par_list, columns=columns)
    return par_df
