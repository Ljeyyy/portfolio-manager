# 📊 Portfolio Manager

Outil minimaliste de gestion de portefeuilles d'investissement.
Stack : FastAPI + SQLite + Alpine.js/Tailwind.

## Prérequis
- Python 3.11+

## Installation

```bash
# 1. Cloner et créer l'environnement virtuel
git clone <repo>
cd portfolio-manager
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate

# 2. Installer les dépendances
pip install -r backend/requirements.txt

# 3. (Optionnel) Configurer les variables d'environnement
cp .env.example .env
# Éditer .env pour changer SECRET_KEY, ADMIN_PASSWORD

# 4. Seeder la base de données (5 clients fictifs)
python -m backend.seed

# 5. Lancer le serveur
uvicorn backend.main:app --reload --port 8000
```

## Accès
- **Frontend** : http://localhost:8000
- **API Docs** : http://localhost:8000/docs
- **Login** : admin / admin123

## Tests
```bash
pytest tests/ -v
```

## Variables d'environnement (.env)
| Variable | Défaut | Description |
|---|---|---|
| `SECRET_KEY` | `change-me-...` | Clé signature JWT |
| `ADMIN_USERNAME` | `admin` | Login admin |
| `ADMIN_PASSWORD` | `admin123` | Mot de passe admin |
| `DATABASE_URL` | `sqlite:///./portfolio.db` | URL base de données |
| `PRICE_CACHE_TTL_SECONDS` | `300` | TTL cache prix (secondes) |

## Passer à PostgreSQL