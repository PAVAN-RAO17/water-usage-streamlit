import pandas as pd

def predict_expected_usage(df, window=7):
    """
    Predict expected water usage using rolling average.
    Falls back to overall mean if data is small.
    """

    if len(df) < window:
        return round(df["usage_liters"].mean(), 2)

    rolling_avg = (
        df["usage_liters"]
        .rolling(window=window)
        .mean()
        .iloc[-1]
    )

    return round(rolling_avg, 2)