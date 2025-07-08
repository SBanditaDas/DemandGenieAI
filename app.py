import streamlit as st
import pandas as pd
from forecasting import forecast_demand
from inventory import get_reorder_recommendations
from simulator import simulate_scenario

# Set page configuration
st.set_page_config(page_title="DemandGenieAI+", layout="wide")

# Optional: Add your logo
st.image("logo.png", width=150)

# Custom header
st.markdown("<h1 style='text-align: center; color: #4B8BBE;'>DemandGenieAI+</h1>", unsafe_allow_html=True)
st.markdown("Smart demand forecasting and inventory planning for MSMEs 🌍")

# Sidebar navigation
st.sidebar.title("🔧 Navigation")
page = st.sidebar.radio("Go to", ["📊 Dashboard", "🧪 Scenario Simulator", "🌐 Load from Google Sheets", "ℹ️ About"])

# Page: Dashboard (Upload CSV)
if page == "📊 Dashboard":
    uploaded_file = st.file_uploader("📤 Upload your sales data (CSV)", type="csv")
    
    # Optional: Download sample CSV
    with open("data/sales.csv", "rb") as file:
        st.download_button("📥 Download Sample CSV", file, file_name="sample_sales.csv")

    if uploaded_file:
        df = pd.read_csv(uploaded_file, parse_dates=['date'])
        sku_list = df['sku'].unique()
        selected_sku = st.selectbox("Select SKU", sku_list)

        forecast_df, fig = forecast_demand(df, selected_sku)
        st.subheader("📈 Demand Forecast")
        st.plotly_chart(fig, use_container_width=True)

        reorder_df = get_reorder_recommendations(forecast_df)
        st.subheader("📦 Reorder Suggestions")
        st.dataframe(reorder_df)

        st.subheader("📬 WhatsApp Alert Preview")
        st.code(f"Hi! Reorder {reorder_df['Suggested Order Qty']} units of {selected_sku} by Friday.")

        st.download_button("📤 Download Forecast (CSV)", forecast_df.to_csv(index=False), file_name="forecast.csv")

# Page: Scenario Simulator
elif page == "🧪 Scenario Simulator":
    st.markdown("### Simulate different supply chain scenarios:")
    delay = st.slider("Supplier Delay (days)", 0, 10, 2)
    promo = st.slider("Promotion Boost (%)", 0, 100, 20)
    if 'forecast_df' in locals():
        sim_result = simulate_scenario(forecast_df, delay, promo)
        st.success(sim_result["Recommendation"])
        st.write(sim_result)
    else:
        st.warning("Please upload data and generate a forecast first in the Dashboard.")

# Page: Load from Google Sheets
elif page == "🌐 Load from Google Sheets":
    st.markdown("### Load sales data from a public Google Sheet (CSV format)")
    sheet_url = st.text_input("Paste your Google Sheets CSV link here:")

    if sheet_url:
        try:
            df = pd.read_csv(sheet_url)
            df['date'] = pd.to_datetime(df['date'])
            sku_list = df['sku'].unique()
            selected_sku = st.selectbox("Select SKU", sku_list)

            forecast_df, fig = forecast_demand(df, selected_sku)
            st.subheader("📈 Demand Forecast")
            st.plotly_chart(fig, use_container_width=True)

            reorder_df = get_reorder_recommendations(forecast_df)
            st.subheader("📦 Reorder Suggestions")
            st.dataframe(reorder_df)

        except Exception as e:
            st.error(f"Failed to load data: {e}")

# Page: About
elif page == "ℹ️ About":
    st.markdown("""
    **DemandGenieAI+** is an AI-powered demand forecasting tool designed for MSMEs.  
    It helps businesses make smarter inventory decisions using causal insights, scenario simulation, and real-time alerts.

    - Built with Streamlit, Prophet, and Plotly  
    - Supports CSV uploads and Google Sheets  
    - Mobile-friendly and easy to use  
    """)
