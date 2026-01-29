from demand_ops.db.base import Base
from demand_ops.db.session import ENGINE
import demand_ops.db.models  # noqa: F401  (ensures models are imported)
import demand_ops.db.metrics_models  # noqa: F401
import demand_ops.db.inventory_models  # noqa: F401
import demand_ops.db.simulation_models  # noqa: F401



def init_db():
    Base.metadata.create_all(bind=ENGINE)

if __name__ == "__main__":
    init_db()
