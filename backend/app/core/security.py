from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone # Adicionado timedelta e timezone
from typing import Any, Union # Adicionado para tipagem
from jose import jwt # Adicionado para manipulação de JWT

from app.core.config import settings # Importa nossas configurações

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica a senha."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Gera o hash da senha."""
    return pwd_context.hash(password)

def create_access_token(subject: Union[str, Any], expires_delta: timedelta = None) -> str:
    """
    Cria um token de acesso JWT.

    Args:
        subject: O "assunto" do token (geralmente o ID ou email do usuário).
        expires_delta: O tempo de vida do token.

    Returns:
        O token JWT codificado como uma string.
    """
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        # Se não for fornecido um delta, usa o padrão das configurações
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    # Dados a serem codificados no token
    to_encode = {"exp": expire, "sub": str(subject)}

    # Codifica o token usando a chave secreta e o algoritmo
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.ALGORITHM)

    return encoded_jwt
