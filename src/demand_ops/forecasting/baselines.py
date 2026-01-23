import pandas as pd

def forecast_naive_last_value(df: pd.DataFrame, horizon_days: int = 14) -> pd.DataFrame:
    last_date = df["date"].max()
    last_value = float(df.sort_values("date")["units"].iloc[-1])

    future_dates = pd.date_range(last_date + pd.Timedelta(days=1), periods=horizon_days, freq="D")
    out = pd.DataFrame({"forecast_date": future_dates, "yhat": last_value})
    return out

def forecast_moving_average(df: pd.DataFrame, window: int = 7, horizon_days: int = 14) -> pd.DataFrame:
    df2 = df.sort_values("date").copy()
    df2["ma"] = df2["units"].rolling(window=window).mean()
    last_date = df2["date"].max()
    last_ma = float(df2["ma"].iloc[-1])

    future_dates = pd.date_range(last_date + pd.Timedelta(days=1), periods=horizon_days, freq="D")
    out = pd.DataFrame({"forecast_date": future_dates, "yhat": last_ma})
    return out
