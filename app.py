import streamlit as st
from datetime import date
from backtest import run_backtest

st.set_page_config(page_title="Quant Strategy Backtest", layout="wide")
st.title("📈 Quant Trading Strategy Backtest")

assets = st.multiselect("Select Assets", [
    "GBPUSD", "EURUSD", "EURGBP", "USDJPY",
    "EURCHF", "OIL", "GOLD", "SILVER"
], default=["GBPUSD", "GOLD"])

col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("Start Date", date(2005, 1, 1))
with col2:
    end_date = st.date_input("End Date", date.today())

if st.button("Run Backtest"):
    with st.spinner("Running backtest..."):
        stats, fig = run_backtest(assets, start_date, end_date)
        st.pyplot(fig)
        st.subheader("📊 Strategy Statistics")
        st.json(stats)
