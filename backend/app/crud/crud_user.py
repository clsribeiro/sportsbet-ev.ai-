from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select # Para SQLAlchemy 1.4+ (FastAPI geralmente usa versões mais recentes)

from app.models.user import User # Nosso modelo SQLAlchemy User
from app.schemas.user import UserCreate # Nosso schema Pydantic para criação de usuário
from app.core.security import get_password_hash # Nossa função de hashing

async def get_user_by_email(db: AsyncSession, *, email: str) -> User | None:
    """
    Busca um usuário pelo email.

    Args:
        db: A sessão assíncrona do banco de dados.
        email: O email a ser buscado.

    Returns:
        O objeto User se encontrado, caso contrário None.
    """
    result = await db.execute(select(User).filter(User.email == email))
    return result.scalars().first()

async def create_user(db: AsyncSession, *, user_in: UserCreate) -> User:
    """
    Cria um novo usuário no banco de dados.

    Args:
        db: A sessão assíncrona do banco de dados.
        user_in: Os dados do usuário a serem criados (do schema Pydantic UserCreate).

    Returns:
        O objeto User criado.
    """
    # Cria um dicionário com os dados do schema, excluindo a senha em texto puro
    # para não tentar passá-la diretamente para o modelo User SQLAlchemy.
    db_user_data = user_in.model_dump(exclude={"password"}) # Pydantic v2
    # Se Pydantic v1: db_user_data = user_in.dict(exclude={"password"})

    hashed_password = get_password_hash(user_in.password)

    db_user = User(**db_user_data, hashed_password=hashed_password)

    db.add(db_user)
    await db.commit() # Salva o usuário no banco
    await db.refresh(db_user) # Atualiza o objeto db_user com dados do banco (ex: ID gerado)
    return db_user

# Poderíamos adicionar outras funções CRUD aqui no futuro:
# async def get_user(db: AsyncSession, user_id: int) -> User | None: ...
# async def update_user(db: AsyncSession, *, db_user: User, user_in: UserUpdate) -> User: ...
# async def delete_user(db: AsyncSession, *, user_id: int) -> User | None: ...
