from sqlalchemy import select
from demand_ops.db.session import get_session
from demand_ops.db.models import Product, Location
from demand_ops.features.queries import load_sales_timeseries
from demand_ops.forecasting.baselines import forecast_naive_last_value, forecast_moving_average
from demand_ops.forecasting.write_forecasts import write_forecasts

def main():
    session = get_session()
    try:
        sku = "SKU-001"
        loc = "BOS-01"

        p = session.execute(select(Product).where(Product.sku == sku)).scalar_one()
        l = session.execute(select(Location).where(Location.code == loc)).scalar_one()

        df = load_sales_timeseries(session, sku=sku, location_code=loc)
        if df.empty:
            raise RuntimeError("No sales data found. Run seed_demo first.")

        f1 = forecast_naive_last_value(df, horizon_days=14)
        f2 = forecast_moving_average(df, window=7, horizon_days=14)

        write_forecasts(session, p.id, l.id, "naive_last", f1.to_dict("records"))
        write_forecasts(session, p.id, l.id, "ma_7", f2.to_dict("records"))

        session.commit()
        print("Forecasts written: naive_last, ma_7")
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

if __name__ == "__main__":
    main()
