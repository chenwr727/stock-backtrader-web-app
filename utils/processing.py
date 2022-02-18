import datetime

import akshare as ak
import backtrader as bt
import backtrader.analyzers as btanalyzers
import pandas as pd
import streamlit as st
import yaml

from .schemas import StrategyBase


@st.cache(allow_output_mutation=True)
def gen_stock_df(ak_params: dict) -> pd.DataFrame:
    """generate stock data

    Args:
        ak_params (dict): akshare kwargs

    Returns:
        pd.DataFrame: _description_
    """
    return ak.stock_zh_a_hist(**ak_params)


@st.cache
def run_backtrader(
    stock_df: pd.DataFrame,
    start_date: datetime.datetime,
    end_date: datetime.datetime,
    start_cash: int,
    commission_fee: float,
    stake: int,
    strategy: StrategyBase,
) -> pd.DataFrame:
    """run backtrader

    Args:
        stock_df (pd.DataFrame): stock data
        start_date (datetime.datetime): back trader from date
        end_date (datetime.datetime): back trader end date
        start_cash (int): back trader start cash
        commission_fee (float): commission fee
        stake (int): stake
        strategy (StrategyBase): strategy name an params

    Returns:
        pd.DataFrame: back trader results
    """
    stock_df.columns = [
        "date",
        "open",
        "close",
        "high",
        "low",
        "volume",
    ]
    stock_df.index = pd.to_datetime(stock_df["date"])
    data = bt.feeds.PandasData(dataname=stock_df, fromdate=start_date, todate=end_date)

    cerebro = bt.Cerebro()
    cerebro.adddata(data)
    cerebro.broker.setcash(start_cash)
    cerebro.broker.setcommission(commission=commission_fee)
    cerebro.addsizer(bt.sizers.FixedSize, stake=stake)
    cerebro.addanalyzer(btanalyzers.SharpeRatio, _name="sharpe")
    cerebro.addanalyzer(btanalyzers.DrawDown, _name="drawdown")
    cerebro.addanalyzer(btanalyzers.Returns, _name="returns")

    strategy_cli = getattr(__import__(f"strategy"), f"{strategy.name}Strategy")
    cerebro.optstrategy(strategy_cli, **strategy.params)
    back = cerebro.run()
    par_list = []
    for x in back:
        par = []
        for param in strategy.params.keys():
            par.append(x[0].params._getkwargs()[param])
        par.extend(
            [
                x[0].analyzers.returns.get_analysis()["rnorm100"],
                x[0].analyzers.drawdown.get_analysis()["max"]["drawdown"],
                x[0].analyzers.sharpe.get_analysis()["sharperatio"],
            ]
        )
        par_list.append(par)
    columns = list(strategy.params.keys())
    columns.extend(["return", "dd", "sharpe"])
    par_df = pd.DataFrame(par_list, columns=columns)
    return par_df


def load_strategy(yaml_file: str) -> dict:
    """load strategy

    Args:
        yaml_file (str): strategy config file path

    Returns:
        dict: strategy
    """
    with open(yaml_file, "r") as f:
        strategy = yaml.safe_load(f)
    return strategy
