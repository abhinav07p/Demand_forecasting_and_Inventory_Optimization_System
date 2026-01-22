import pandas as pd
from sqlalchemy import select
from sqlalchemy.orm import Session

from demand_ops.db.models import SalesDaily, Product, Location

def load_sales_timeseries(
    session: Session,
    sku: str,
    location_code: str,
) -> pd.DataFrame:
    """
    Returns a tidy time series dataframe:
    columns: [date, units, price, sku, location]
    """
    stmt = (
        select(
            SalesDaily.sales_date.label("date"),
            SalesDaily.units_sold.label("units"),
            SalesDaily.unit_price.label("price"),
            Product.sku.label("sku"),
            Location.code.label("location"),
        )
        .join(Product, Product.id == SalesDaily.product_id)
        .join(Location, Location.id == SalesDaily.location_id)
        .where(Product.sku == sku)
        .where(Location.code == location_code)
        .order_by(SalesDaily.sales_date.asc())
    )

    rows = session.execute(stmt).all()
    df = pd.DataFrame(rows, columns=["date", "units", "price", "sku", "location"])
    if not df.empty:
        df["date"] = pd.to_datetime(df["date"])
        df["units"] = df["units"].astype(int)
        df["price"] = df["price"].astype(float)
    return df
