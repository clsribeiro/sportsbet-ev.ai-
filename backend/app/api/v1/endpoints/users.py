from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession # Para tipagem da dependência da sessão de DB

# Importações dos nossos módulos
import app.schemas.user as user_schemas # Nossos schemas Pydantic para User
import app.crud.crud_user as crud_user   # Nossas funções CRUD para User
from app.db.session import get_db_session  # Nossa dependência para obter a sessão de DB

router = APIRouter()

@router.post(
    "/", # Ou você pode usar "/register" se preferir um nome mais explícito
    response_model=user_schemas.UserRead, # O que a API retornará (NÃO inclui a senha)
    status_code=status.HTTP_201_CREATED, # Código de status para criação bem-sucedida
    summary="Registrar um novo usuário",
    tags=["Usuários"] # Agrupa este endpoint na documentação da API
)
async def register_new_user(
    *,
    db: AsyncSession = Depends(get_db_session), # Injeta a sessão do banco de dados
    user_in: user_schemas.UserCreate # Dados do usuário vindo do corpo da requisição (validados pelo Pydantic)
):
    """
    Cria um novo usuário no sistema.
    - **email**: Email do usuário (deve ser único).
    - **password**: Senha do usuário (mínimo de 8 caracteres).
    - **full_name**: (Opcional) Nome completo do usuário.
    """
    # Verifica se o usuário já existe no banco de dados
    existing_user = await crud_user.get_user_by_email(db, email=user_in.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Um usuário com este email já existe no sistema.",
        )

    # Cria o usuário
    user = await crud_user.create_user(db=db, user_in=user_in)

    # Retorna o usuário criado (sem a senha hasheada, conforme definido em UserRead)
    return user
