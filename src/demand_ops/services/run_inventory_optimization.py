from sqlalchemy import select
from pyomo.environ import SolverFactory

from demand_ops.db.session import get_session
from demand_ops.db.models import Product, Location
from demand_ops.db.forecast_models import ForecastDaily
from demand_ops.db.inventory_models import InventoryPolicy
from demand_ops.optimization.model import build_inventory_model
from demand_ops.optimization.params import InventoryParams


def main():
    session = get_session()
    try:
        sku = "SKU-001"
        loc = "BOS-01"
        model_name = "ma_7"

        p = session.execute(select(Product).where(Product.sku == sku)).scalar_one()
        l = session.execute(select(Location).where(Location.code == loc)).scalar_one()

        # simple aggregate demand (next 7 days)
        forecasts = session.execute(
            select(ForecastDaily.yhat)
            .where(ForecastDaily.product_id == p.id)
            .where(ForecastDaily.location_id == l.id)
            .where(ForecastDaily.model_name == model_name)
        ).scalars().all()

        total_demand = sum(forecasts)

        params = InventoryParams()

        model = build_inventory_model(
            demand_forecast=total_demand,
            holding_cost=params.holding_cost,
            stockout_cost=params.stockout_cost,
        )

        solver = SolverFactory("highs")
        solver.solve(model)

        policy = InventoryPolicy(
            product_id=p.id,
            location_id=l.id,
            as_of_date=max([f for f in session.execute(
                select(ForecastDaily.forecast_date)
            ).scalars()]),
            model_name=model_name,
            reorder_qty=float(model.order_qty.value),
        )

        session.add(policy)
        session.commit()

        print("Optimal reorder quantity:", policy.reorder_qty)

    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


if __name__ == "__main__":
    main()
