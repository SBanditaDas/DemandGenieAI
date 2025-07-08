def get_reorder_recommendations(forecast_df, lead_time=5, safety_factor=1.65):
    avg_demand = forecast_df['yhat'][-lead_time:].mean()
    std_dev = forecast_df['yhat'][-lead_time:].std()
    safety_stock = safety_factor * std_dev
    reorder_point = avg_demand * lead_time + safety_stock

    return {
        'Reorder Point': round(reorder_point),
        'Safety Stock': round(safety_stock),
        'Suggested Order Qty': round(reorder_point)
    }