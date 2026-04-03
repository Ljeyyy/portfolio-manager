# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from backend.database import Base, engine
from backend.routes import auth, clients, assets, dashboard

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Portfolio Manager",
    description="Outil de gestion de portefeuilles d'investissement",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(clients.router)
app.include_router(assets.router)
app.include_router(dashboard.router)

app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

@app.get("/", include_in_schema=False)
def serve_frontend():
    return FileResponse("frontend/index.html")

@app.get("/app", include_in_schema=False)
def serve_app():
    return FileResponse("frontend/dashboard.html")

@app.get("/health")
def health_check():
    return {"status": "ok", "version": "1.0.0"}