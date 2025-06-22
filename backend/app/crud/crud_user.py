from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from uuid import UUID
from typing import List

from app.models.user import User
from app.models.role import Role # Importe o modelo Role
from app.schemas.user import UserCreate

async def get_user_by_id(db: AsyncSession, *, user_id: UUID) -> User | None:
    """Busca um único utilizador pelo seu ID, carregando os seus planos (roles)."""
    result = await db.execute(
        select(User)
        .where(User.id == user_id)
        .options(selectinload(User.roles)) # Carregamento otimizado dos roles
    )
    return result.scalars().first()

async def get_user_by_email(db: AsyncSession, *, email: str) -> User | None:
    """Busca um utilizador pelo email."""
    result = await db.execute(select(User).filter(User.email == email))
    return result.scalars().first()

async def get_users(db: AsyncSession, *, skip: int = 0, limit: int = 100) -> List[User]:
    """Busca uma lista de todos os utilizadores."""
    result = await db.execute(
        select(User)
        .order_by(User.email.asc())
        .options(selectinload(User.roles)) # Opcional: carregar roles para a lista
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()

async def create_user(db: AsyncSession, *, user_in: UserCreate) -> User:
    """Cria um novo utilizador no banco de dados."""
    db_user_data = user_in.model_dump(exclude={"password"})
    hashed_password = get_password_hash(user_in.password)
    db_user = User(**db_user_data, hashed_password=hashed_password)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def update_user_roles(db: AsyncSession, *, user: User, role_ids: List[int]) -> User:
    """Atualiza os planos (roles) de um utilizador."""
    # Busca todos os objetos de role correspondentes aos IDs fornecidos
    result = await db.execute(select(Role).where(Role.id.in_(role_ids)))
    roles = result.scalars().all()

    # Substitui a lista de roles do utilizador pela nova lista
    user.roles = roles

    db.add(user)
    await db.commit()
    await db.refresh(user)

    # Recarrega o utilizador com os roles para a resposta
    updated_user = await get_user_by_id(db, user_id=user.id)
    return updated_user

# Não se esqueça de importar get_password_hash se ainda estiver a ser usado aqui
from app.core.security import get_password_hash
