from datetime import date
from sqlalchemy import Integer, Date, String, Float, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from demand_ops.db.base import Base

class ForecastDaily(Base):
    __tablename__ = "forecast_daily"
    __table_args__ = (
        UniqueConstraint("product_id", "location_id", "forecast_date", "model_name", name="uq_forecast_daily"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("dim_product.id"), nullable=False, index=True)
    location_id: Mapped[int] = mapped_column(ForeignKey("dim_location.id"), nullable=False, index=True)

    forecast_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    yhat: Mapped[float] = mapped_column(Float, nullable=False)
    model_name: Mapped[str] = mapped_column(String(64), nullable=False)
