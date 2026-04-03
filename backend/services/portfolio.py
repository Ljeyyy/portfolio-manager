# backend/services/portfolio.py
from typing import List, Dict
from backend.models.asset import Asset
from backend.services.pricing import get_prices_batch

def calculate_portfolio(assets: List[Asset], use_mock: bool = False) -> Dict:
    """
    Calcule la valeur totale, le P&L global et l'allocation par classe d'actif.

    Returns:
        {
            "total_value": float,
            "total_cost": float,
            "total_pnl": float,
            "total_pnl_pct": float,
            "positions": [...],
            "allocation": { "action": %, "ETF": %, "crypto": % }
        }
    """
    if not assets:
        return {
            "total_value": 0.0, "total_cost": 0.0,
            "total_pnl": 0.0, "total_pnl_pct": 0.0,
            "positions": [], "allocation": {}
        }

    # Batch fetch des prix pour minimiser les appels API
    tickers = list({a.ticker for a in assets})
    prices  = get_prices_batch(tickers, use_mock=use_mock)

    positions      = []
    total_value    = 0.0
    total_cost     = 0.0
    class_values: Dict[str, float] = {}

    for asset in assets:
        current_price = prices.get(asset.ticker, asset.purchase_price)
        cost          = asset.purchase_price * asset.quantity
        value         = current_price * asset.quantity
        pnl           = value - cost
        pnl_pct       = (pnl / cost * 100) if cost > 0 else 0.0

        total_value += value
        total_cost  += cost
        class_values[asset.asset_class] = class_values.get(asset.asset_class, 0.0) + value

        positions.append({
            "id":             asset.id,
            "ticker":         asset.ticker,
            "name":           asset.name,
            "asset_class":    asset.asset_class,
            "quantity":       asset.quantity,
            "purchase_price": asset.purchase_price,
            "current_price":  round(current_price, 4),
            "cost":           round(cost, 2),
            "value":          round(value, 2),
            "pnl":            round(pnl, 2),
            "pnl_pct":        round(pnl_pct, 2),
            "currency":       asset.currency,
        })

    # Allocation en pourcentage par classe d'actif
    allocation = {
        cls: round(val / total_value * 100, 2)
        for cls, val in class_values.items()
    } if total_value > 0 else {}

    total_pnl     = total_value - total_cost
    total_pnl_pct = (total_pnl / total_cost * 100) if total_cost > 0 else 0.0

    return {
        "total_value":    round(total_value, 2),
        "total_cost":     round(total_cost, 2),
        "total_pnl":      round(total_pnl, 2),
        "total_pnl_pct":  round(total_pnl_pct, 2),
        "positions":      positions,
        "allocation":     allocation,
    }