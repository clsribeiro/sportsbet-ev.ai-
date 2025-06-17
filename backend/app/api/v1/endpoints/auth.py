from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm # Formulário padrão para login
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta

import app.schemas.token as token_schemas
import app.crud.crud_user as crud_user
from app.db.session import get_db_session
from app.core.security import verify_password, create_access_token
from app.core.config import settings

router = APIRouter()

@router.post("/login", response_model=token_schemas.Token, summary="Obter Token de Acesso", tags=["Autenticação"])
async def login_for_access_token(
    db: AsyncSession = Depends(get_db_session),
    form_data: OAuth2PasswordRequestForm = Depends() # Usa o formulário padrão do FastAPI
):
    """
    Autentica o usuário e retorna um token de acesso.
    """
    # 1. Busca o usuário no banco pelo email (que no OAuth2PasswordRequestForm vem no campo 'username')
    user = await crud_user.get_user_by_email(db, email=form_data.username)

    # 2. Verifica se o usuário existe e se a senha está correta
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 3. Cria o token de acesso
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=user.id, expires_delta=access_token_expires
    )

    # 4. Retorna o token
    return {"access_token": access_token, "token_type": "bearer"}
