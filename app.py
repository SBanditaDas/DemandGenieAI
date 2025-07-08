import streamlit as st
import pandas as pd
from forecasting import forecast_demand
from inventory import get_reorder_recommendations
from simulator import simulate_scenario

st.set_page_config(page_title="DemandGenieAI+", layout="wide")
st.title("📊 DemandGenieAI+ Dashboard")
st.markdown("Smart demand forecasting and inventory planning for MSMEs")

uploaded_file = st.file_uploader("Upload your sales data (CSV)", type="csv")
if uploaded_file:
    df = pd.read_csv(uploaded_file, parse_dates=['date'])
    sku_list = df['sku'].unique()
    selected_sku = st.selectbox("Select SKU", sku_list)

    st.subheader("📈 Demand Forecast")
    forecast_df, fig = forecast_demand(df, selected_sku)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("📦 Reorder Suggestions")
    reorder_df = get_reorder_recommendations(forecast_df)
    st.dataframe(reorder_df)

    st.subheader("🧪 Scenario Simulator")
    delay = st.slider("Supplier Delay (days)", 0, 10, 2)
    promo = st.slider("Promotion Boost (%)", 0, 100, 20)
    sim_result = simulate_scenario(forecast_df, delay, promo)
    st.write(sim_result)

    st.download_button("📤 Download Forecast (CSV)", forecast_df.to_csv(index=False), file_name="forecast.csv")