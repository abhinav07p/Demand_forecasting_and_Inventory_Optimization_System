from sqlalchemy.orm import Session
from demand_ops.db.forecast_models import ForecastDaily

def write_forecasts(
    session: Session,
    product_id: int,
    location_id: int,
    model_name: str,
    forecast_rows: list[dict],
):
    for r in forecast_rows:
        session.add(ForecastDaily(
            product_id=product_id,
            location_id=location_id,
            model_name=model_name,
            forecast_date=r["forecast_date"].date() if hasattr(r["forecast_date"], "date") else r["forecast_date"],
            yhat=float(r["yhat"]),
        ))
