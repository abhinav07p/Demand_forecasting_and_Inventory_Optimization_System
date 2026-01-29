from datetime import date
from sqlalchemy import Integer, Date, Float, ForeignKey, UniqueConstraint, String
from sqlalchemy.orm import Mapped, mapped_column
from demand_ops.db.base import Base

class InventoryPolicy(Base):
    __tablename__ = "inventory_policy"
    __table_args__ = (
        UniqueConstraint("product_id", "location_id", "as_of_date", "model_name",
                         name="uq_inventory_policy"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("dim_product.id"), nullable=False)
    location_id: Mapped[int] = mapped_column(ForeignKey("dim_location.id"), nullable=False)

    as_of_date: Mapped[date] = mapped_column(Date, nullable=False)
    model_name: Mapped[str] = mapped_column(String(64), nullable=False)

    reorder_qty: Mapped[float] = mapped_column(Float, nullable=False)
