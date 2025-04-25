import unittest
from datetime import datetime
from typing import Type

import akshare as ak
import backtrader as bt
import backtrader.analyzers as btanalyzers
import pandas as pd

from strategy.base import BaseStrategy
from utils.load import load_strategy


class StrategyTest(unittest.TestCase):
    """策略测试基类"""

    def setUp(self):
        """测试前准备工作，加载数据和设置回测环境"""

        # 加载股票历史数据
        stock_hfq_df = ak.stock_zh_a_hist(symbol="600070", adjust="hfq", start_date="20230101", end_date="20250101")
        stock_hfq_df = stock_hfq_df[["日期", "开盘", "收盘", "最高", "最低", "成交量"]]
        stock_hfq_df.columns = ["date", "open", "close", "high", "low", "volume"]
        stock_hfq_df.index = pd.to_datetime(stock_hfq_df["date"])
        start_date = datetime(2024, 1, 1)
        end_date = datetime(2025, 1, 1)
        data = bt.feeds.PandasData(dataname=stock_hfq_df, fromdate=start_date, todate=end_date)

        # 设置回测引擎
        self.cerebro = cerebro = bt.Cerebro()
        cerebro.adddata(data)
        cerebro.broker.setcash(1000000)
        cerebro.broker.setcommission(commission=0.001)
        cerebro.addsizer(bt.sizers.FixedSize, stake=100)

        # 添加分析器
        cerebro.addanalyzer(btanalyzers.SharpeRatio, _name="sharpe")
        cerebro.addanalyzer(btanalyzers.DrawDown, _name="drawdown")
        cerebro.addanalyzer(btanalyzers.Returns, _name="returns")

        # 加载策略配置
        self.strategys = load_strategy("./config/strategy.yaml")
        self.result = None

    def tearDown(self):
        """测试后验证结果"""
        self.assertIsInstance(self.result, pd.DataFrame)
        print(f"测试结果:\n{self.result}")


def run_back_trader(cerebro: bt.Cerebro, strategy: Type[BaseStrategy], **kwargs) -> pd.DataFrame:
    """运行回测

    Args:
        cerebro (bt.Cerebro): 回测引擎
        strategy (Type[BaseStrategy]): 策略类
        **kwargs: 策略参数

    Returns:
        pd.DataFrame: 回测结果
    """
    # 添加优化策略
    cerebro.optstrategy(strategy, **kwargs)

    # 运行回测
    back = cerebro.run(maxcpus=1)

    # 处理回测结果
    par_list = []
    for x in back:
        # 收集策略参数
        par = []
        for param in kwargs.keys():
            par.append(x[0].params._getkwargs()[param])

        # 添加性能指标
        par.extend(
            [
                x[0].analyzers.returns.get_analysis()["rnorm100"],
                x[0].analyzers.drawdown.get_analysis()["max"]["drawdown"],
                x[0].analyzers.sharpe.get_analysis()["sharperatio"],
            ]
        )
        par_list.append(par)

    # 创建结果数据框
    columns = list(kwargs.keys())
    columns.extend(["return", "dd", "sharpe"])
    par_df = pd.DataFrame(par_list, columns=columns)
    return par_df
