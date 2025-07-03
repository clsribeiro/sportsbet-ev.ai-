from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload, subqueryload
from uuid import UUID
from typing import List, Dict, Any, Union

from app.models.user import User
from app.models.role import Role
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash

async def update_user(
    db: AsyncSession, *, db_user: User, user_in: Union[UserUpdate, Dict[str, Any]]
) -> User:
    """Atualiza os dados de um utilizador."""
    if isinstance(user_in, dict):
        update_data = user_in
    else:
        update_data = user_in.model_dump(exclude_unset=True)

    if "password" in update_data and update_data["password"]:
        hashed_password = get_password_hash(update_data["password"])
        del update_data["password"]
        update_data["hashed_password"] = hashed_password
    
    for field, value in update_data.items():
        setattr(db_user, field, value)
    
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def create_user(db: AsyncSession, *, user_in: UserCreate) -> User:
    db_user_data = user_in.model_dump(exclude={"password"})
    hashed_password = get_password_hash(user_in.password)
    db_user = User(**db_user_data, hashed_password=hashed_password)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def get_user_by_id_with_permissions(db: AsyncSession, *, user_id: UUID) -> User | None:
    result = await db.execute(
        select(User).where(User.id == user_id).options(selectinload(User.roles).subqueryload(Role.permissions))
    )
    return result.scalars().unique().first()

async def get_user_by_email(db: AsyncSession, *, email: str) -> User | None:
    result = await db.execute(select(User).filter(User.email == email))
    return result.scalars().first()
    
async def get_users(db: AsyncSession, *, skip: int = 0, limit: int = 100) -> List[User]:
    result = await db.execute(
        select(User).order_by(User.email.asc()).options(selectinload(User.roles)).offset(skip).limit(limit)
    )
    return result.scalars().all()

async def update_user_roles(db: AsyncSession, *, user: User, role_ids: List[int]) -> User:
    result = await db.execute(select(Role).where(Role.id.in_(role_ids)))
    user.roles = result.scalars().all()
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return await get_user_by_id_with_permissions(db, user_id=user.id)
