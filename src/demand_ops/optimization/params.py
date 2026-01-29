from dataclasses import dataclass

@dataclass
class InventoryParams:
    holding_cost: float = 0.5     # per unit per day
    stockout_cost: float = 5.0    # per unit
    lead_time_days: int = 3
