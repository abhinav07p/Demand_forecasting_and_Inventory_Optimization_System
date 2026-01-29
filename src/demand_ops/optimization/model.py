from pyomo.environ import (
    ConcreteModel, Var, NonNegativeReals, Objective, minimize
)

def build_inventory_model(
    demand_forecast: float,
    holding_cost: float,
    stockout_cost: float,
):
    m = ConcreteModel()

    m.order_qty = Var(domain=NonNegativeReals)
    m.stockout = Var(domain=NonNegativeReals)

    # Cost = holding + stockout
    m.obj = Objective(
        expr=holding_cost * m.order_qty +
             stockout_cost * m.stockout,
        sense=minimize
    )

    # Demand balance
    m.demand_constraint = (
        m.order_qty + m.stockout >= demand_forecast
    )

    return m
