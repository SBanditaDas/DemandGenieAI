from prophet import Prophet
import pandas as pd
import plotly.graph_objects as go

def forecast_demand(df, sku):
    sku_df = df[df['sku'] == sku][['date', 'sales']].rename(columns={'date': 'ds', 'sales': 'y'})
    model = Prophet()
    model.fit(sku_df)
    future = model.make_future_dataframe(periods=30)
    forecast = model.predict(future)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat'], name='Forecast'))
    fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat_upper'], name='Upper Bound', line=dict(dash='dot')))
    fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat_lower'], name='Lower Bound', line=dict(dash='dot')))
    fig.update_layout(title=f"Forecast for {sku}", xaxis_title="Date", yaxis_title="Sales")

    return forecast, fig