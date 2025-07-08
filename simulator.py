def simulate_scenario(forecast_df, delay_days, promo_boost):
    adjusted_forecast = forecast_df.copy()
    adjusted_forecast['yhat'] *= (1 + promo_boost / 100)

    projected_stockout_day = delay_days + 1 if promo_boost > 30 else delay_days + 3
    return {
        "Adjusted Demand (Next 7 Days)": round(adjusted_forecast['yhat'][:7].sum()),
        "Projected Stockout Day": f"Day {projected_stockout_day}",
        "Recommendation": "Increase reorder quantity by 20%" if promo_boost > 30 else "No change needed"
    }