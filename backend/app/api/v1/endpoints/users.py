from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

import app.schemas.user as user_schemas
import app.crud.crud_user as crud_user
from app.db.session import get_db_session
from app.api.deps.current_user import get_current_user
from app.models.user import User
from app.core.security import verify_password

router = APIRouter()

@router.get("/me", response_model=user_schemas.UserRead, summary="Obter dados do utilizador atual", tags=["Utilizadores"])
async def read_current_user(
    current_user: User = Depends(get_current_user)
):
    """Retorna as informações do utilizador que está atualmente autenticado."""
    return current_user

@router.put("/me", response_model=user_schemas.UserRead, summary="Atualizar dados do utilizador atual", tags=["Utilizadores"])
async def update_current_user(
    *,
    db: AsyncSession = Depends(get_db_session),
    user_in: user_schemas.UserUpdate,
    current_user: User = Depends(get_current_user)
):
    """Atualiza as informações do utilizador autenticado (ex: nome completo)."""
    user = await crud_user.update_user(db=db, db_user=current_user, user_in=user_in)
    return user

# --- NOVO ENDPOINT ---
@router.post("/me/password", status_code=status.HTTP_204_NO_CONTENT, summary="Alterar a senha do utilizador atual", tags=["Utilizadores"])
async def update_current_user_password(
    *,
    db: AsyncSession = Depends(get_db_session),
    password_data: user_schemas.UserPasswordUpdate,
    current_user: User = Depends(get_current_user)
):
    """
    Altera a senha do utilizador autenticado.
    """
    # 1. Verifica se a senha atual fornecida está correta
    if not verify_password(password_data.current_password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A senha atual está incorreta.",
        )
    
    # 2. Atualiza a senha no banco de dados
    await crud_user.update_user(
        db=db, db_user=current_user, user_in={"password": password_data.new_password}
    )
    # Retorna 204 No Content para indicar sucesso sem corpo de resposta
    return

@router.post(
    "/",
    response_model=user_schemas.UserRead,
    status_code=status.HTTP_201_CREATED,
    summary="Registar um novo utilizador",
    tags=["Utilizadores"]
)
async def register_new_user(
    *,
    db: AsyncSession = Depends(get_db_session),
    user_in: user_schemas.UserCreate
):
    """Cria um novo utilizador no sistema."""
    existing_user = await crud_user.get_user_by_email(db, email=user_in.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Um utilizador com este email já existe no sistema.",
        )
    user = await crud_user.create_user(db=db, user_in=user_in)
    return user
