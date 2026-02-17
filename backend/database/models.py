from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, func
import os

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql+asyncpg://postgres:postgres@localhost:5432/organ')

engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()


class Run(Base):
    __tablename__ = 'runs'
    id = Column(String, primary_key=True)
    created_at = Column(DateTime, server_default=func.now())
    params = Column(JSON)
    metrics = Column(JSON)


class Molecule(Base):
    __tablename__ = 'molecules'
    id = Column(Integer, primary_key=True, autoincrement=True)
    run_id = Column(String)
    smiles = Column(String)
    qed = Column(Float)
    sa = Column(Float)
    diversity = Column(Float)
