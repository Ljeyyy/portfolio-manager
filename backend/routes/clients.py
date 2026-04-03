# backend/routes/clients.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from backend.database import get_db
from backend.models.client import Client
from backend.schemas.client import ClientCreate, ClientUpdate, ClientResponse
from backend.auth.jwt import get_current_user

router = APIRouter(prefix="/api/clients", tags=["Clients"])

@router.get("/", response_model=List[ClientResponse])
def list_clients(
    skip: int = 0, limit: int = 100,
    db: Session = Depends(get_db),
    _: dict = Depends(get_current_user)
):
    """Liste tous les clients avec pagination."""
    return db.query(Client).offset(skip).limit(limit).all()

@router.post("/", response_model=ClientResponse, status_code=status.HTTP_201_CREATED)
def create_client(
    payload: ClientCreate,
    db: Session = Depends(get_db),
    _: dict = Depends(get_current_user)
):
    """Crée un nouveau client."""
    existing = db.query(Client).filter(Client.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email déjà utilisé")
    client = Client(**payload.model_dump())
    db.add(client)
    db.commit()
    db.refresh(client)
    return client

@router.get("/{client_id}", response_model=ClientResponse)
def get_client(
    client_id: int,
    db: Session = Depends(get_db),
    _: dict = Depends(get_current_user)
):
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client introuvable")
    return client

@router.put("/{client_id}", response_model=ClientResponse)
def update_client(
    client_id: int,
    payload: ClientUpdate,
    db: Session = Depends(get_db),
    _: dict = Depends(get_current_user)
):
    """Mise à jour partielle (PATCH-like) d'un client."""
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client introuvable")
    for field, value in payload.model_dump(exclude_none=True).items():
        setattr(client, field, value)
    db.commit()
    db.refresh(client)
    return client

@router.delete("/{client_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_client(
    client_id: int,
    db: Session = Depends(get_db),
    _: dict = Depends(get_current_user)
):
    """Supprime un client et toutes ses positions (cascade)."""
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client introuvable")
    db.delete(client)
    db.commit()