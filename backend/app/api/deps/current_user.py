from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import ValidationError
from uuid import UUID

from app.core.config import settings
from app.db.session import get_db_session
from app.models.user import User
import app.crud.crud_user as crud_user
import app.schemas.token as token_schemas

# Define o esquema de autenticação OAuth2.
# O tokenUrl aponta para o nosso endpoint de login. Isso é usado principalmente
# para a documentação interativa da API (Swagger UI).
reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"/api/v1/auth/login"
)

async def get_current_user(
    db: AsyncSession = Depends(get_db_session), token: str = Depends(reusable_oauth2)
) -> User:
    """
    Dependência para obter o usuário atual a partir de um token JWT.

    Valida o token, decodifica, e busca o usuário no banco de dados.
    Levanta exceções HTTP se o token for inválido ou o usuário não for encontrado.
    """
    try:
        # Decodifica o token JWT
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        # O "sub" (subject) do nosso token é o ID do usuário
        user_id: UUID = UUID(payload.get("sub"))
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Não foi possível validar as credenciais (ID de usuário ausente)",
            )
        # Você poderia adicionar aqui um schema Pydantic para validar o payload do token
        # token_data = token_schemas.TokenPayload(**payload)
    except (JWTError, ValidationError, AttributeError): # Adicionado AttributeError para UUID
        # Se o token for inválido (expirado, malformado, etc.)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Não foi possível validar as credenciais (token inválido)",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Busca o usuário no banco de dados pelo ID extraído do token
    user = await crud_user.get_user_by_id(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado.")

    # Opcional: Verificar se o usuário está ativo
    # if not user.is_active:
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Usuário inativo.")

    return user

# --- NOVA DEPENDÊNCIA ADICIONADA ---
def get_current_superuser(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Dependência que verifica se o utilizador atual é um superutilizador.
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Este recurso requer privilégios de administrador.",
        )
    return current_user

