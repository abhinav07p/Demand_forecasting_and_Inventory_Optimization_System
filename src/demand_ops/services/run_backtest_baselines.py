from datetime import timedelta

import pandas as pd
from sqlalchemy import select

from demand_ops.db.session import get_session
from demand_ops.db.models import Product, Location
from demand_ops.db.metrics_models import ForecastMetric
from demand_ops.features.queries import load_sales_timeseries
from demand_ops.forecasting.baselines import forecast_naive_last_value, forecast_moving_average
from demand_ops.forecasting.metrics import mape, smape, rmse

def backtest(df: pd.DataFrame, horizon_days: int = 7, min_train_days: int = 30):
    df = df.sort_values("date").copy()
    if len(df) < (min_train_days + horizon_days):
        raise RuntimeError("Not enough history for backtest")

    cut = df["date"].max() - pd.Timedelta(days=horizon_days)
    train = df[df["date"] <= cut]
    test = df[df["date"] > cut]

    f_naive = forecast_naive_last_value(train, horizon_days=horizon_days)
    f_ma7 = forecast_moving_average(train, window=7, horizon_days=horizon_days)

    # align on dates
    merged = test[["date", "units"]].rename(columns={"date": "forecast_date"})
    merged = merged.merge(f_naive, on="forecast_date", how="left", suffixes=("", "_naive"))
    merged = merged.rename(columns={"yhat": "yhat_naive"})
    merged = merged.merge(f_ma7, on="forecast_date", how="left")
    merged = merged.rename(columns={"yhat": "yhat_ma7"})

    y = merged["units"].tolist()
    y_naive = merged["yhat_naive"].tolist()
    y_ma7 = merged["yhat_ma7"].tolist()

    return {
        "as_of_date": cut.date(),
        "naive_last": {"mape": mape(y, y_naive), "smape": smape(y, y_naive), "rmse": rmse(y, y_naive)},
        "ma_7": {"mape": mape(y, y_ma7), "smape": smape(y, y_ma7), "rmse": rmse(y, y_ma7)},
    }

def main():
    session = get_session()
    try:
        sku = "SKU-001"
        loc = "BOS-01"

        p = session.execute(select(Product).where(Product.sku == sku)).scalar_one()
        l = session.execute(select(Location).where(Location.code == loc)).scalar_one()

        df = load_sales_timeseries(session, sku=sku, location_code=loc)
        res = backtest(df, horizon_days=7, min_train_days=30)

        as_of = res["as_of_date"]
        for model_name in ["naive_last", "ma_7"]:
            r = res[model_name]
            session.add(ForecastMetric(
                product_id=p.id,
                location_id=l.id,
                as_of_date=as_of,
                model_name=model_name,
                mape=r["mape"],
                smape=r["smape"],
                rmse=r["rmse"],
            ))

        session.commit()
        print("Backtest metrics written:", res)
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

if __name__ == "__main__":
    main()
