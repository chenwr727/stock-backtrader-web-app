import streamlit as st
from streamlit_echarts import st_pyecharts

from charts import draw_pro_kline, draw_result_bar
from frames import akshare_selector_ui, backtrader_selector_ui, params_selector_ui
from utils.load import load_strategy
from utils.logs import logger
from utils.processing import gen_stock_df, run_backtrader
from utils.schemas import StrategyBase

st.set_page_config(page_title="backtrader", page_icon=":chart_with_upwards_trend:", layout="wide")


def main():
    ak_params = akshare_selector_ui()
    bt_params = backtrader_selector_ui()
    if ak_params.symbol:
        stock_df = gen_stock_df(ak_params)
        if stock_df.empty:
            st.error("Get stock data failed!")
            return

        st.subheader("Kline")
        kline = draw_pro_kline(stock_df)
        st_pyecharts(kline, height="500px")

        st.subheader("Strategy")
        name = st.selectbox("strategy", list(strategy_dict.keys()))
        submitted, params = params_selector_ui(strategy_dict[name])
        if submitted:
            logger.info(f"akshare: {ak_params}")
            logger.info(f"backtrader: {bt_params}")
            stock_df = stock_df.rename(
                columns={
                    "日期": "date",
                    "开盘": "open",
                    "收盘": "close",
                    "最高": "high",
                    "最低": "low",
                    "成交量": "volume",
                }
            )
            strategy = StrategyBase(name=name, params=params)
            par_df = run_backtrader(stock_df, strategy, bt_params)
            st.dataframe(par_df.style.highlight_max(subset=par_df.columns[-3:]))
            bar = draw_result_bar(par_df)
            st_pyecharts(bar, height="500px")


strategy_dict = load_strategy("./config/strategy.yaml")

if __name__ == "__main__":
    main()
