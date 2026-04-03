# backend/seed.py
"""Script de seed — 5 clients fictifs avec portefeuilles réalistes."""
from backend.database import SessionLocal, Base, engine
from backend.models.client import Client
from backend.models.asset import Asset

Base.metadata.create_all(bind=engine)

CLIENTS = [
    {"name": "Sophie Moreau",   "email": "sophie.moreau@email.com",   "risk_profile": "conservateur", "total_capital": 50000.0},
    {"name": "Thomas Dupont",   "email": "thomas.dupont@email.com",   "risk_profile": "modéré",       "total_capital": 120000.0},
    {"name": "Camille Petit",   "email": "camille.petit@email.com",   "risk_profile": "agressif",     "total_capital": 80000.0},
    {"name": "Marc Lefebvre",   "email": "marc.lefebvre@email.com",   "risk_profile": "modéré",       "total_capital": 200000.0},
    {"name": "Isabelle Roux",   "email": "isabelle.roux@email.com",   "risk_profile": "conservateur", "total_capital": 35000.0},
]

PORTFOLIOS = {
    "sophie.moreau@email.com": [
        {"ticker": "SPY",     "name": "S&P 500 ETF",      "asset_class": "ETF",    "quantity": 20,   "purchase_price": 480.0,  "currency": "USD"},
        {"ticker": "QQQ",     "name": "Nasdaq 100 ETF",   "asset_class": "ETF",    "quantity": 10,   "purchase_price": 400.0,  "currency": "USD"},
    ],
    "thomas.dupont@email.com": [
        {"ticker": "AAPL",    "name": "Apple Inc.",        "asset_class": "action", "quantity": 50,   "purchase_price": 165.0,  "currency": "USD"},
        {"ticker": "MSFT",    "name": "Microsoft Corp.",   "asset_class": "action", "quantity": 30,   "purchase_price": 380.0,  "currency": "USD"},
        {"ticker": "SPY",     "name": "S&P 500 ETF",       "asset_class": "ETF",    "quantity": 15,   "purchase_price": 490.0,  "currency": "USD"},
        {"ticker": "BTC-USD", "name": "Bitcoin",           "asset_class": "crypto", "quantity": 0.5,  "purchase_price": 45000.0,"currency": "USD"},
    ],
    "camille.petit@email.com": [
        {"ticker": "NVDA",    "name": "NVIDIA Corp.",      "asset_class": "action", "quantity": 40,   "purchase_price": 550.0,  "currency": "USD"},
        {"ticker": "BTC-USD", "name": "Bitcoin",           "asset_class": "crypto", "quantity": 1.2,  "purchase_price": 42000.0,"currency": "USD"},
        {"ticker": "ETH-USD", "name": "Ethereum",          "asset_class": "crypto", "quantity": 8.0,  "purchase_price": 2800.0, "currency": "USD"},
    ],
    "marc.lefebvre@email.com": [
        {"ticker": "AAPL",    "name": "Apple Inc.",        "asset_class": "action", "quantity": 100,  "purchase_price": 150.0,  "currency": "USD"},
        {"ticker": "GOOGL",   "name": "Alphabet Inc.",     "asset_class": "action", "quantity": 60,   "purchase_price": 140.0,  "currency": "USD"},
        {"ticker": "SPY",     "name": "S&P 500 ETF",       "asset_class": "ETF",    "quantity": 50,   "purchase_price": 450.0,  "currency": "USD"},
        {"ticker": "QQQ",     "name": "Nasdaq 100 ETF",    "asset_class": "ETF",    "quantity": 40,   "purchase_price": 380.0,  "currency": "USD"},
        {"ticker": "BTC-USD", "name": "Bitcoin",           "asset_class": "crypto", "quantity": 2.0,  "purchase_price": 38000.0,"currency": "USD"},
    ],
    "isabelle.roux@email.com": [
        {"ticker": "SPY",     "name": "S&P 500 ETF",       "asset_class": "ETF",    "quantity": 10,   "purchase_price": 470.0,  "currency": "USD"},
        {"ticker": "AMZN",    "name": "Amazon.com Inc.",   "asset_class": "action", "quantity": 15,   "purchase_price": 170.0,  "currency": "USD"},
    ],
}

def seed():
    db = SessionLocal()
    try:
        # Éviter le double seed
        if db.query(Client).count() > 0:
            print("DB déjà seedée — skip.")
            return

        for client_data in CLIENTS:
            client = Client(**client_data)
            db.add(client)
            db.flush()  # Pour obtenir l'ID avant commit

            for asset_data in PORTFOLIOS.get(client_data["email"], []):
                asset = Asset(client_id=client.id, **asset_data)
                db.add(asset)

        db.commit()
        print(f"✅ Seed OK — {len(CLIENTS)} clients insérés.")
    except Exception as e:
        db.rollback()
        print(f"❌ Erreur seed: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed()