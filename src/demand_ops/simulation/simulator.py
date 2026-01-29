def simulate_inventory(
    demand_series: list[float],
    initial_inventory: float,
    reorder_qty: float,
    holding_cost: float,
    stockout_cost: float,
):
    inventory = initial_inventory
    total_demand = 0.0
    total_fulfilled = 0.0
    total_stockout = 0.0
    holding_cost_total = 0.0

    for d in demand_series:
        total_demand += d

        fulfilled = min(inventory, d)
        stockout = max(0.0, d - inventory)

        total_fulfilled += fulfilled
        total_stockout += stockout

        inventory = inventory - fulfilled + reorder_qty
        holding_cost_total += inventory * holding_cost

    return {
        "total_demand": total_demand,
        "total_fulfilled": total_fulfilled,
        "stockouts": total_stockout,
        "holding_cost": holding_cost_total,
        "stockout_cost": total_stockout * stockout_cost,
    }
