from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload, subqueryload
from uuid import UUID
from typing import List, Dict, Any, Union

from app.models.user import User
from app.models.role import Role
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash

# --- FUNÇÃO MODIFICADA ---
# Agora lida com a atualização de senha de forma segura
async def update_user(
    db: AsyncSession, *, db_user: User, user_in: Union[UserUpdate, Dict[str, Any]]
) -> User:
    """Atualiza os dados de um utilizador."""
    if isinstance(user_in, dict):
        update_data = user_in
    else:
        # Pega apenas os campos que foram enviados para não apagar os existentes
        update_data = user_in.model_dump(exclude_unset=True)

    # Se uma nova senha for fornecida no dicionário, faz o hash dela
    if "password" in update_data and update_data["password"]:
        hashed_password = get_password_hash(update_data["password"])
        del update_data["password"] # Remove a senha em texto puro
        update_data["hashed_password"] = hashed_password
    
    for field, value in update_data.items():
        setattr(db_user, field, value)
    
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def create_user(db: AsyncSession, *, user_in: UserCreate) -> User:
    """Cria um novo utilizador no banco de dados."""
    db_user_data = user_in.model_dump(exclude={"password"})
    hashed_password = get_password_hash(user_in.password)
    db_user = User(**db_user_data, hashed_password=hashed_password)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

# --- Funções existentes (sem alterações) ---

async def get_user_by_id_with_permissions(db: AsyncSession, *, user_id: UUID) -> User | None:
    result = await db.execute(
        select(User)
        .where(User.id == user_id)
        .options(selectinload(User.roles).subqueryload(Role.permissions))
    )
    return result.scalars().unique().first()

async def get_user_by_id(db: AsyncSession, *, user_id: UUID) -> User | None:
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalars().first()

async def get_user_by_email(db: AsyncSession, *, email: str) -> User | None:
    result = await db.execute(select(User).filter(User.email == email))
    return result.scalars().first()
    
async def get_users(db: AsyncSession, *, skip: int = 0, limit: int = 100) -> List[User]:
    result = await db.execute(
        select(User)
        .order_by(User.email.asc())
        .options(selectinload(User.roles))
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()

async def update_user_roles(db: AsyncSession, *, user: User, role_ids: List[int]) -> User:
    result = await db.execute(select(Role).where(Role.id.in_(role_ids)))
    roles = result.scalars().all()
    user.roles = roles
    db.add(user)
    await db.commit()
    await db.refresh(user)
    updated_user = await get_user_by_id_with_permissions(db, user_id=user.id)
    return updated_user
