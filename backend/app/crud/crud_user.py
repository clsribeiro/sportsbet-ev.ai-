from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload, subqueryload
from uuid import UUID
from typing import List

from app.models.user import User
from app.models.role import Role
from app.schemas.user import UserCreate
from app.core.security import get_password_hash

# --- NOVA FUNÇÃO OTIMIZADA ---
async def get_user_by_id_with_permissions(db: AsyncSession, *, user_id: UUID) -> User | None:
    """
    Busca um único utilizador pelo seu ID, carregando otimizadamente
    os seus roles e as permissões de cada role.
    Esta é a função preferencial para obter o utilizador atual autenticado.
    """
    result = await db.execute(
        select(User)
        .where(User.id == user_id)
        .options(
            # Carrega os 'roles' do utilizador e, para cada role,
            # pré-carrega as suas 'permissions' numa segunda query (subqueryload).
            # Isto evita o problema de N+1 queries.
            selectinload(User.roles).subqueryload(Role.permissions)
        )
    )
    # .unique() é importante ao usar joined/selectin loading para evitar duplicatas
    return result.scalars().unique().first()


async def get_user_by_id(db: AsyncSession, *, user_id: UUID) -> User | None:
    """
    Busca um único utilizador pelo seu ID (sem carregar permissões).
    Útil para quando apenas os detalhes básicos do utilizador são necessários.
    """
    result = await db.execute(
        select(User).where(User.id == user_id)
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
        .options(selectinload(User.roles)) # Carrega os roles para a lista de utilizadores
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
    result = await db.execute(select(Role).where(Role.id.in_(role_ids)))
    roles = result.scalars().all()
    
    user.roles = roles
    
    db.add(user)
    await db.commit()
    await db.refresh(user)
    
    # Recarrega o utilizador com os roles e permissões para a resposta
    updated_user = await get_user_by_id_with_permissions(db, user_id=user.id)
    return updated_user

