import datetime

import akshare as ak
import backtrader as bt
import backtrader.analyzers as btanalyzers
import pandas as pd
import streamlit as st
import yaml
from streamlit_echarts import st_pyecharts

from charts import draw_pro_kline, draw_result_bar
from frames import akshare_selector_ui, backtrader_selector_ui, params_selector_ui
from modules.schemas import StrategyBase

# from utils.logs import LOGGER


st.set_page_config(page_title="backtrader")


def main():
    ak_params = akshare_selector_ui()
    backtrader_params = backtrader_selector_ui()
    if ak_params["symbol"]:
        stock_df = gen_stock_df(ak_params)

        st.subheader("Kline")
        # kline = draw_pro_kline(stock_df)
        # st_pyecharts(kline, height="500px")

        st.subheader("Strategy")
        name = st.selectbox("strategy", list(strategys.keys()))
        submitted, params = params_selector_ui(strategys[name])
        if submitted:
            backtrader_params.update(
                {
                    "stock_df": stock_df.iloc[:, :6],
                    "strategy": StrategyBase(name=name, params=params),
                }
            )
            par_df = run_backtrader(**backtrader_params)
            st.dataframe(par_df.style.highlight_max(subset=par_df.columns[-3:]))
            bar = draw_result_bar(par_df)
            st_pyecharts(bar, height="500px")


@st.cache(allow_output_mutation=True)
def gen_stock_df(ak_params: dict) -> pd.DataFrame:
    """generate stock data

    :param ak_params: dict.
    :return: pd.DataFrame.
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

    :param stock_df: pd.DataFrame. stock data
    :param start_date: datetime.datetime. back trader from date
    :param end_date: datetime.datetime. back trader end date
    :param start_cash: int. back trader start cash
    :param commission_fee: float. commission fee
    :param stake: int. stake
    :param strategy: StrategyBase. strategy name an params
    :return: None.
    """
    cerebro = bt.Cerebro()
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
    cerebro.adddata(data)
    cerebro.broker.setcash(start_cash)
    cerebro.broker.setcommission(commission=commission_fee)
    cerebro.addsizer(bt.sizers.FixedSize, stake=stake)
    cerebro.addanalyzer(btanalyzers.SharpeRatio, _name="sharpe")
    cerebro.addanalyzer(btanalyzers.DrawDown, _name="drawdown")
    cerebro.addanalyzer(btanalyzers.Returns, _name="returns")

    print("start cash: %.2f" % cerebro.broker.getvalue())
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
    print("end cash: %.2f" % cerebro.broker.getvalue())
    return par_df


def load_strategys(yaml_file):
    with open(yaml_file, "r") as f:
        strategys = yaml.safe_load(f)
    return strategys


strategys = load_strategys("./config/strategy.yaml")

if __name__ == "__main__":
    main()
