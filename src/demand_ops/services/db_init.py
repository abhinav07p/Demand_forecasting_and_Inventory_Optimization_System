from demand_ops.db.base import Base
from demand_ops.db.session import ENGINE
import demand_ops.db.models  # noqa: F401  (ensures models are imported)

def init_db():
    Base.metadata.create_all(bind=ENGINE)

if __name__ == "__main__":
    init_db()
