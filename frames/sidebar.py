import datetime

import streamlit as st

from utils.schemas import AkshareParams, BacktraderParams


def akshare_selector_ui() -> AkshareParams:
    """akshare params

    :return: AkshareParams
    """
    st.sidebar.markdown("# Akshare Config")
    symbol = st.sidebar.text_input("symbol")
    period = st.sidebar.selectbox("period", ("daily", "weekly", "monthly"))
    start_date = st.sidebar.date_input("start date", datetime.date(1970, 1, 1))
    start_date = start_date.strftime("%Y%m%d")
    end_date = st.sidebar.date_input("end date", datetime.datetime.today())
    end_date = end_date.strftime("%Y%m%d")
    adjust = st.sidebar.selectbox("adjust", ("qfq", "hfq", ""))
    return AkshareParams(
        symbol=symbol,
        period=period,
        start_date=start_date,
        end_date=end_date,
        adjust=adjust,
    )


def backtrader_selector_ui() -> BacktraderParams:
    """backtrader params

    :return: BacktraderParams
    """
    st.sidebar.markdown("# BackTrader Config")
    start_date = st.sidebar.date_input("backtrader start date", datetime.date(2000, 1, 1))
    end_date = st.sidebar.date_input("backtrader end date", datetime.datetime.today())
    start_cash = st.sidebar.number_input("start cash", min_value=0, value=100000, step=10000)
    commission_fee = st.sidebar.number_input("commission fee", min_value=0.0, max_value=1.0, value=0.001, step=0.0001)
    stake = st.sidebar.number_input("stake", min_value=0, value=100, step=10)
    return BacktraderParams(
        start_date=start_date,
        end_date=end_date,
        start_cash=start_cash,
        commission_fee=commission_fee,
        stake=stake,
    )
