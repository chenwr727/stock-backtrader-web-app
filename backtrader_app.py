import streamlit as st
from streamlit_echarts import st_pyecharts

from charts import draw_pro_kline, draw_result_bar
from frames import akshare_selector_ui, backtrader_selector_ui, params_selector_ui
from utils.logs import LOGGER
from utils.processing import gen_stock_df, load_strategy, run_backtrader
from utils.schemas import StrategyBase

st.set_page_config(page_title="backtrader")


def main():
    ak_params = akshare_selector_ui()
    backtrader_params = backtrader_selector_ui()
    if ak_params["symbol"]:
        stock_df = gen_stock_df(ak_params)

        st.subheader("Kline")
        kline = draw_pro_kline(stock_df)
        st_pyecharts(kline, height="500px")

        st.subheader("Strategy")
        name = st.selectbox("strategy", list(strategy.keys()))
        submitted, params = params_selector_ui(strategy[name])
        if submitted:
            LOGGER.info(f"akshare: {ak_params}")
            LOGGER.info(f"backtrader: {backtrader_params}")
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


strategy = load_strategy("./config/strategy.yaml")

if __name__ == "__main__":
    main()
