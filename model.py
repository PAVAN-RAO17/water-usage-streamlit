import pandas as pd
from prophet import Prophet

def predict_expected_usage(df):
    prophet_df = df[['date', 'usage_liters']].rename(
        columns={'date': 'ds', 'usage_liters': 'y'}
    )

    model = Prophet()
    model.fit(prophet_df)


    future = model.make_future_dataframe(periods=1)
    forecast = model.predict(future)

    expected = forecast.iloc[-1]['yhat']
    return round(expected,2)