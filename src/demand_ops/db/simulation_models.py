from datetime import date
from sqlalchemy import Integer, Date, Float, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from demand_ops.db.base import Base

class InventorySimulation(Base):
    __tablename__ = "inventory_simulation"
    __table_args__ = (
        UniqueConstraint("product_id", "location_id", "as_of_date", "policy_name",
                         name="uq_inventory_simulation"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("dim_product.id"), nullable=False)
    location_id: Mapped[int] = mapped_column(ForeignKey("dim_location.id"), nullable=False)

    as_of_date: Mapped[date] = mapped_column(Date, nullable=False)
    policy_name: Mapped[str] = mapped_column(String(64), nullable=False)

    total_demand: Mapped[float] = mapped_column(Float, nullable=False)
    total_fulfilled: Mapped[float] = mapped_column(Float, nullable=False)
    stockouts: Mapped[float] = mapped_column(Float, nullable=False)
    holding_cost: Mapped[float] = mapped_column(Float, nullable=False)
    stockout_cost: Mapped[float] = mapped_column(Float, nullable=False)
