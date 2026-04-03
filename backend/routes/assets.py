# backend/routes/assets.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from backend.database import get_db
from backend.models.asset import Asset
from backend.models.client import Client
from backend.schemas.asset import AssetCreate, AssetUpdate, AssetResponse
from backend.auth.jwt import get_current_user

router = APIRouter(prefix="/api/assets", tags=["Assets"])

def _get_client_or_404(client_id: int, db: Session) -> Client:
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client introuvable")
    return client

@router.get("/client/{client_id}", response_model=List[AssetResponse])
def list_assets(
    client_id: int,
    db: Session = Depends(get_db),
    _: dict = Depends(get_current_user)
):
    _get_client_or_404(client_id, db)
    return db.query(Asset).filter(Asset.client_id == client_id).all()

@router.post("/", response_model=AssetResponse, status_code=status.HTTP_201_CREATED)
def create_asset(
    payload: AssetCreate,
    db: Session = Depends(get_db),
    _: dict = Depends(get_current_user)
):
    _get_client_or_404(payload.client_id, db)
    asset = Asset(**payload.model_dump())
    db.add(asset)
    db.commit()
    db.refresh(asset)
    return asset

@router.put("/{asset_id}", response_model=AssetResponse)
def update_asset(
    asset_id: int,
    payload: AssetUpdate,
    db: Session = Depends(get_db),
    _: dict = Depends(get_current_user)
):
    asset = db.query(Asset).filter(Asset.id == asset_id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset introuvable")
    for field, value in payload.model_dump(exclude_none=True).items():
        setattr(asset, field, value)
    db.commit()
    db.refresh(asset)
    return asset

@router.delete("/{asset_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_asset(
    asset_id: int,
    db: Session = Depends(get_db),
    _: dict = Depends(get_current_user)
):
    asset = db.query(Asset).filter(Asset.id == asset_id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset introuvable")
    db.delete(asset)
    db.commit()