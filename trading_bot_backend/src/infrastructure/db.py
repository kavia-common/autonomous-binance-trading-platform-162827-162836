"""
SQLite database setup using SQLAlchemy ORM.

Provides:
- Engine and session factory
- Declarative models for User, Strategy, Trade, UserSetting
- Database initialization and utility helpers
"""
from __future__ import annotations

import os
from contextlib import contextmanager
from datetime import datetime
from typing import Generator

from sqlalchemy import (
    create_engine,
    String,
    Boolean,
    DateTime,
    Float,
    Enum as SAEnum,
    ForeignKey,
    JSON,
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker, Mapped, mapped_column

from src.core.config import get_settings
from src.domain.enums import TradingMode, OrderSide, OrderType

Base = declarative_base()

# SQLite engine; when database_url is empty or sqlite path not provided, fallback to local file.
def _resolve_db_url() -> str:
    settings = get_settings()
    url = os.getenv("DATABASE_URL", settings.database_url).strip()
    if not url:
        # Default to local sqlite file in container root
        return "sqlite:///./app.db"
    return url

DATABASE_URL = _resolve_db_url()
# For SQLite need check_same_thread=False for multi-threaded FastAPI
engine = create_engine(
    DATABASE_URL,
    echo=False,
    future=True,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, future=True)


class UserORM(Base):
    __tablename__ = "users"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    full_name: Mapped[str | None] = mapped_column(String, nullable=True)
    password_hash: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    strategies: Mapped[list["StrategyORM"]] = relationship("StrategyORM", back_populates="user", cascade="all, delete-orphan")
    trades: Mapped[list["TradeORM"]] = relationship("TradeORM", back_populates="user", cascade="all, delete-orphan")
    settings: Mapped[list["UserSettingORM"]] = relationship("UserSettingORM", back_populates="user", cascade="all, delete-orphan")


class UserSettingORM(Base):
    __tablename__ = "user_settings"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), index=True, nullable=False)
    key: Mapped[str] = mapped_column(String, nullable=False)
    value: Mapped[str] = mapped_column(String, nullable=False)

    user: Mapped["UserORM"] = relationship("UserORM", back_populates="settings")


class StrategyORM(Base):
    __tablename__ = "strategies"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), index=True, nullable=False)

    name: Mapped[str] = mapped_column(String, nullable=False)
    parameters: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    enabled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    user: Mapped["UserORM"] = relationship("UserORM", back_populates="strategies")


class TradeORM(Base):
    __tablename__ = "trades"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), index=True, nullable=False)

    symbol: Mapped[str] = mapped_column(String, index=True, nullable=False)
    side: Mapped[OrderSide] = mapped_column(SAEnum(OrderSide), nullable=False)
    type: Mapped[OrderType] = mapped_column(SAEnum(OrderType), nullable=False)
    quantity: Mapped[float] = mapped_column(Float, nullable=False)
    price: Mapped[float | None] = mapped_column(Float, nullable=True)
    mode: Mapped[TradingMode] = mapped_column(SAEnum(TradingMode), default=TradingMode.DEMO, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    user: Mapped["UserORM"] = relationship("UserORM", back_populates="trades")


def init_db() -> None:
    """Create database tables."""
    Base.metadata.create_all(bind=engine)


@contextmanager
def db_session() -> Generator:
    """Provide a transactional scope for DB operations."""
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
