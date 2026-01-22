from sqlalchemy import select
from sqlalchemy.orm import Session

from demand_ops.db.models import Product, Location, SalesDaily


class ProductRepo:
    def __init__(self, session: Session):
        self.session = session

    def upsert(self, sku: str, name: str) -> Product:
        obj = self.session.execute(
            select(Product).where(Product.sku == sku)
        ).scalar_one_or_none()

        if obj:
            obj.name = name
            return obj

        obj = Product(sku=sku, name=name)
        self.session.add(obj)
        return obj


class LocationRepo:
    def __init__(self, session: Session):
        self.session = session

    def upsert(self, code: str, name: str) -> Location:
        obj = self.session.execute(
            select(Location).where(Location.code == code)
        ).scalar_one_or_none()

        if obj:
            obj.name = name
            return obj

        obj = Location(code=code, name=name)
        self.session.add(obj)
        return obj


class SalesRepo:
    def __init__(self, session: Session):
        self.session = session

    def add(self, sale: SalesDaily) -> SalesDaily:
        self.session.add(sale)
        return sale
