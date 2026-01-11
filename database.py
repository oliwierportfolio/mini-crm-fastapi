from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Enum as SqlEnum
)
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime
from enum import Enum as PyEnum

engine = create_engine("sqlite:///crm.db", echo=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()


class UserRole(str, PyEnum):
    admin = "admin"
    salesperson = "handlowiec"


class LeadDB(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    status = Column(
        SqlEnum("new", "contacted", "meeting", "client", "lost", name="lead_status"),
        nullable=False
    )
    created_at = Column(DateTime, default=datetime.utcnow)


class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    role = Column(SqlEnum(UserRole, native_enum=False), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class LeadHistoryDB(Base):
    __tablename__ = "lead_history"

    id = Column(Integer, primary_key=True, index=True)
    lead_id = Column(Integer, ForeignKey("leads.id", ondelete="CASCADE"), nullable=False)
    old_status = Column(String, nullable=False)
    new_status = Column(String, nullable=False)
    changed_at = Column(DateTime, default=datetime.utcnow)


Base.metadata.create_all(engine)
