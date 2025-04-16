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
    if not assets:
        st.error("Please select at least one asset.")
    elif start_date >= end_date:
        st.error("Start date must be before end date.")
    else:
        with st.spinner("Running backtest..."):
            try:
                stats, fig = run_backtest(assets, start_date, end_date)
                st.pyplot(fig)
                st.subheader("📊 Strategy Statistics")
                
                # Display Total Return prominently
                st.metric("Total Return", f"{stats['Total Return (%)']}%")
                
                # Display other stats
                st.json({
                    "Sharpe Ratio": stats["Sharpe Ratio"],
                    "Max Drawdown": stats["Max Drawdown"],
                    "Returns Analysis": stats["Returns Analysis"]
                })
            except Exception as e:
                st.error(f"Backtest failed: {str(e)}")