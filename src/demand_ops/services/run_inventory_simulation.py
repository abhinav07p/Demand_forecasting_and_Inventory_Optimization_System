from sqlalchemy import select

from demand_ops.db.session import get_session
from demand_ops.db.models import Product, Location
from demand_ops.db.forecast_models import ForecastDaily
from demand_ops.db.inventory_models import InventoryPolicy
from demand_ops.db.simulation_models import InventorySimulation
from demand_ops.optimization.params import InventoryParams
from demand_ops.simulation.simulator import simulate_inventory


def main():
    session = get_session()
    try:
        sku = "SKU-001"
        loc = "BOS-01"
        policy_name = "optimized_ma7"

        p = session.execute(select(Product).where(Product.sku == sku)).scalar_one()
        l = session.execute(select(Location).where(Location.code == loc)).scalar_one()

        forecasts = session.execute(
            select(ForecastDaily.yhat, ForecastDaily.forecast_date)
            .where(ForecastDaily.product_id == p.id)
            .where(ForecastDaily.location_id == l.id)
            .where(ForecastDaily.model_name == "ma_7")
            .order_by(ForecastDaily.forecast_date)
        ).all()

        demand_series = [float(f[0]) for f in forecasts]
        as_of_date = max(f[1] for f in forecasts)

        policy = session.execute(
            select(InventoryPolicy)
            .where(InventoryPolicy.product_id == p.id)
            .where(InventoryPolicy.location_id == l.id)
        ).scalar_one()

        params = InventoryParams()

        result = simulate_inventory(
            demand_series=demand_series,
            initial_inventory=policy.reorder_qty,
            reorder_qty=policy.reorder_qty,
            holding_cost=params.holding_cost,
            stockout_cost=params.stockout_cost,
        )

        sim = InventorySimulation(
            product_id=p.id,
            location_id=l.id,
            as_of_date=as_of_date,
            policy_name=policy_name,
            **result,
        )

        session.add(sim)
        session.commit()

        print("Simulation results:", result)

    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


if __name__ == "__main__":
    main()
