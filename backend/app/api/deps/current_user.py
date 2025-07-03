from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from pydantic import ValidationError
from uuid import UUID

from app.core.config import settings
from app.db.session import get_db_session
from app.models.user import User
from app.models.role import Role
import app.crud.crud_user as crud_user

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"/api/v1/auth/login"
)

async def _get_user_from_token(token: str, db: AsyncSession) -> User | None:
    """Lógica central para descodificar um token e buscar o utilizador."""
    if not token:
        return None
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        user_id: UUID = UUID(payload.get("sub"))
        if user_id is None:
            return None
    except (JWTError, ValidationError, AttributeError):
        return None
    
    user = await crud_user.get_user_by_id_with_permissions(db, user_id=user_id)
    return user

async def get_current_user(
    db: AsyncSession = Depends(get_db_session), token: str = Depends(reusable_oauth2)
) -> User:
    """Dependência para rotas HTTP."""
    user = await _get_user_from_token(token=token, db=db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Não foi possível validar as credenciais",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

def get_current_superuser(current_user: User = Depends(get_current_user)) -> User:
    """Verifica se o utilizador é um superutilizador."""
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Este recurso requer privilégios de administrador.",
        )
    return current_user

def require_permission(permission_name: str):
    """Verifica se o utilizador tem uma permissão específica."""
    async def permission_checker(
        current_user: User = Depends(get_current_user)
    ) -> User:
        if current_user.is_superuser:
            return current_user
        user_permissions = {
            permission.name 
            for role in current_user.roles 
            for permission in role.permissions
        }
        if permission_name not in user_permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Você não tem permissão para aceder a este recurso.",
            )
        return current_user
    return permission_checker
