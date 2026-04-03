# backend/models/asset.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.database import Base

class Asset(Base):
    __tablename__ = "assets"

    id             = Column(Integer, primary_key=True, index=True)
    client_id      = Column(Integer, ForeignKey("clients.id"), nullable=False, index=True)
    ticker         = Column(String(20), nullable=False)   # ex: "AAPL", "BTC-USD"
    name           = Column(String(100), nullable=False)  # ex: "Apple Inc."
    asset_class    = Column(String(20), nullable=False)   # action/ETF/crypto
    quantity       = Column(Float, nullable=False)
    purchase_price = Column(Float, nullable=False)        # Prix moyen d'achat (€/$)
    currency       = Column(String(5), default="USD")
    created_at     = Column(DateTime(timezone=True), server_default=func.now())

    client = relationship("Client", back_populates="assets")