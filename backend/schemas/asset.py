# backend/schemas/asset.py
from pydantic import BaseModel, field_validator
from typing import Optional
from enum import Enum
from datetime import datetime

class AssetClass(str, Enum):
    action = "action"
    etf    = "ETF"
    crypto = "crypto"

class AssetBase(BaseModel):
    ticker:         str
    name:           str
    asset_class:    AssetClass
    quantity:       float
    purchase_price: float
    currency:       str = "USD"

    @field_validator("quantity", "purchase_price")
    @classmethod
    def must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("La valeur doit être strictement positive")
        return v

    @field_validator("ticker")
    @classmethod
    def ticker_upper(cls, v):
        return v.upper().strip()

class AssetCreate(AssetBase):
    client_id: int

class AssetUpdate(BaseModel):
    name:           Optional[str]        = None
    quantity:       Optional[float]      = None
    purchase_price: Optional[float]      = None
    asset_class:    Optional[AssetClass] = None

class AssetResponse(AssetBase):
    id:         int
    client_id:  int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True