# backend/schemas/client.py
from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from enum import Enum
from datetime import datetime

class RiskProfile(str, Enum):
    conservateur = "conservateur"
    modere       = "modéré"
    agressif     = "agressif"

class ClientBase(BaseModel):
    name:          str
    email:         EmailStr
    risk_profile:  RiskProfile
    total_capital: float

    @field_validator("total_capital")
    @classmethod
    def capital_positive(cls, v):
        if v < 0:
            raise ValueError("Le capital doit être positif")
        return v

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Le nom ne peut pas être vide")
        return v.strip()

class ClientCreate(ClientBase):
    pass

class ClientUpdate(BaseModel):
    name:          Optional[str]          = None
    email:         Optional[EmailStr]     = None
    risk_profile:  Optional[RiskProfile]  = None
    total_capital: Optional[float]        = None

class ClientResponse(ClientBase):
    id:         int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True