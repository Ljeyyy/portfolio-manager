# backend/routes/auth.py
from fastapi import APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends
from backend.config import settings
from backend.auth.jwt import create_access_token

router = APIRouter(prefix="/api/auth", tags=["Auth"])

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Authentification simple username/password.
    Retourne un JWT Bearer token.
    """
    # Auth simple monoutilisateur (admin) — extensible à DB users
    if (form_data.username != settings.ADMIN_USERNAME or
            form_data.password != settings.ADMIN_PASSWORD):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Identifiants incorrects",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = create_access_token(data={"sub": form_data.username})
    return {"access_token": token, "token_type": "bearer"}