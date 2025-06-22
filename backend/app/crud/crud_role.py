from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from app.models.role import Role
from app.schemas.role import RoleCreate

async def create_role(db: AsyncSession, *, role_in: RoleCreate) -> Role:
    """Cria um novo Role (Plano) se ele não existir."""
    result = await db.execute(select(Role).filter(Role.name == role_in.name))
    existing_role = result.scalars().first()
    if existing_role:
        return existing_role

    db_role = Role(**role_in.model_dump())
    db.add(db_role)
    await db.commit()
    await db.refresh(db_role)
    return db_role

async def get_roles(db: AsyncSession, *, skip: int = 0, limit: int = 100) -> List[Role]:
    """Busca uma lista de todos os Roles."""
    result = await db.execute(select(Role).order_by(Role.id).offset(skip).limit(limit))
    return result.scalars().all()
