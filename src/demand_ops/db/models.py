from datetime import date
from sqlalchemy import String, Integer, Date, Numeric, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

class Product(Base):
    __tablename__ = "dim_product"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sku: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)

class Location(Base):
    __tablename__ = "dim_location"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)

class SalesDaily(Base):
    __tablename__ = "fact_sales_daily"
    __table_args__ = (UniqueConstraint("product_id", "location_id", "sales_date", name="uq_sales_daily"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("dim_product.id"), nullable=False, index=True)
    location_id: Mapped[int] = mapped_column(ForeignKey("dim_location.id"), nullable=False, index=True)

    sales_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    units_sold: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_price: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)

    product: Mapped["Product"] = relationship()
    location: Mapped["Location"] = relationship()
