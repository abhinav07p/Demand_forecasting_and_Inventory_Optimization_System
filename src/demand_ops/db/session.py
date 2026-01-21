from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from demand_ops.config import get_settings

def create_engine_from_settings():
    settings = get_settings()
    return create_engine(
        settings.sqlalchemy_url(),
        pool_pre_ping=True,
        future=True,
    )

ENGINE = create_engine_from_settings()

SessionLocal = sessionmaker(
    bind=ENGINE,
    autoflush=False,
    autocommit=False,
    future=True,
)

def get_session():
    return SessionLocal()
