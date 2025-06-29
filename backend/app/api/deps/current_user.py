from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload # Importar selectinload para o carregamento otimizado
from pydantic import ValidationError
from uuid import UUID

from app.core.config import settings
from app.db.session import get_db_session
from app.models.user import User
from app.crud import crud_user

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"/api/v1/auth/login"
)

async def get_current_user(
    db: AsyncSession = Depends(get_db_session), token: str = Depends(reusable_oauth2)
) -> User:
    """
    Dependência para obter o utilizador atual a partir de um token JWT.
    Valida o token e busca o utilizador no banco de dados, incluindo os seus roles e permissões.
    """
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        user_id: UUID = UUID(payload.get("sub"))
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Não foi possível validar as credenciais (ID de utilizador ausente)",
            )
    except (JWTError, ValidationError, AttributeError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Não foi possível validar as credenciais (token inválido)",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # --- MODIFICAÇÃO IMPORTANTE: Carregar roles e permissões ---
    # Vamos modificar o crud_user.get_user_by_id para carregar os relacionamentos
    user = await crud_user.get_user_by_id_with_permissions(db, user_id=user_id)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Utilizador não encontrado.")

    return user


def get_current_superuser(current_user: User = Depends(get_current_user)) -> User:
    """Dependência que verifica se o utilizador atual é um superutilizador."""
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Este recurso requer privilégios de administrador.",
        )
    return current_user


# --- NOVA DEPENDÊNCIA DE PERMISSÃO ---
def require_permission(permission_name: str):
    """
    Cria uma dependência que verifica se o utilizador atual tem uma permissão específica.
    """
    async def permission_checker(
        current_user: User = Depends(get_current_user)
    ) -> User:
        # Superutilizadores têm todas as permissões
        if current_user.is_superuser:
            return current_user

        # Obtém um conjunto (set) de todos os nomes de permissão do utilizador
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