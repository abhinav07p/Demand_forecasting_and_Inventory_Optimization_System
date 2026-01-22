from demand_ops.db.session import get_session
from demand_ops.features.queries import load_sales_timeseries

def main():
    session = get_session()
    try:
        df = load_sales_timeseries(session, sku="SKU-001", location_code="BOS-01")
        print(df.head(10).to_string(index=False))
        print(f"\nrows={len(df)}")
    finally:
        session.close()

if __name__ == "__main__":
    main()
