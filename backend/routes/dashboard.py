# backend/routes/dashboard.py
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
import io
from backend.database import get_db
from backend.models.client import Client
from backend.models.asset import Asset
from backend.services.portfolio import calculate_portfolio
from backend.services.export import generate_csv
from backend.auth.jwt import get_current_user

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])

@router.get("/{client_id}")
def get_dashboard(
    client_id: int,
    mock: bool = False,
    db: Session = Depends(get_db),
    _: dict = Depends(get_current_user)
):
    """
    Retourne la synthèse complète du portefeuille d'un client :
    valeur totale, P&L, allocation par classe d'actif, positions détaillées.
    Paramètre ?mock=true pour utiliser des prix fictifs (offline/tests).
    """
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client introuvable")

    assets    = db.query(Asset).filter(Asset.client_id == client_id).all()
    portfolio = calculate_portfolio(assets, use_mock=mock)

    return {
        "client": {
            "id":            client.id,
            "name":          client.name,
            "email":         client.email,
            "risk_profile":  client.risk_profile,
            "total_capital": client.total_capital,
        },
        "portfolio": portfolio,
    }

@router.get("/{client_id}/export/csv")
def export_csv(
    client_id: int,
    mock: bool = False,
    db: Session = Depends(get_db),
    _: dict = Depends(get_current_user)
):
    """Exporte le portefeuille en CSV téléchargeable."""
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client introuvable")

    assets    = db.query(Asset).filter(Asset.client_id == client_id).all()
    portfolio = calculate_portfolio(assets, use_mock=mock)
    csv_data  = generate_csv(client.name, portfolio)

    filename  = f"portfolio_{client.name.replace(' ', '_')}_{client.id}.csv"
    return StreamingResponse(
        io.StringIO(csv_data),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )