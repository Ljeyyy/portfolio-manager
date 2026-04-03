# backend/models/client.py
from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.database import Base

class Client(Base):
    __tablename__ = "clients"

    id             = Column(Integer, primary_key=True, index=True)
    name           = Column(String(100), nullable=False, index=True)
    email          = Column(String(150), unique=True, nullable=False)
    risk_profile   = Column(String(20), nullable=False)  # conservateur/modéré/agressif
    total_capital  = Column(Float, nullable=False, default=0.0)
    created_at     = Column(DateTime(timezone=True), server_default=func.now())
    updated_at     = Column(DateTime(timezone=True), onupdate=func.now())

    # Relation 1-N vers les positions
    assets = relationship("Asset", back_populates="client", cascade="all, delete-orphan")