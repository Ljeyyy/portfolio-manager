# backend/services/export.py
import csv
import io
from typing import List, Dict

def generate_csv(client_name: str, portfolio_data: Dict) -> str:
    """
    Génère un CSV du portefeuille d'un client.
    Retourne le contenu CSV sous forme de string.
    """
    output = io.StringIO()
    writer = csv.writer(output, delimiter=";")

    # En-tête du rapport
    writer.writerow(["Portfolio Report", client_name])
    writer.writerow([])
    writer.writerow([
        "Ticker", "Nom", "Classe", "Quantité",
        "Prix Achat", "Prix Actuel", "Coût Total",
        "Valeur Actuelle", "P&L (€/$)", "P&L (%)", "Devise"
    ])

    # Lignes positions
    for pos in portfolio_data.get("positions", []):
        writer.writerow([
            pos["ticker"],
            pos["name"],
            pos["asset_class"],
            pos["quantity"],
            pos["purchase_price"],
            pos["current_price"],
            pos["cost"],
            pos["value"],
            pos["pnl"],
            f"{pos['pnl_pct']}%",
            pos["currency"],
        ])

    # Résumé
    writer.writerow([])
    writer.writerow(["TOTAL", "",  "", "",  "", "",
                     portfolio_data["total_cost"],
                     portfolio_data["total_value"],
                     portfolio_data["total_pnl"],
                     f"{portfolio_data['total_pnl_pct']}%", ""])

    # Allocation
    writer.writerow([])
    writer.writerow(["Allocation par classe"])
    for cls, pct in portfolio_data.get("allocation", {}).items():
        writer.writerow([cls, f"{pct}%"])

    return output.getvalue()