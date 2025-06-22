from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from app.models.permission import Permission
from app.schemas.permission import PermissionCreate

async def create_permission(db: AsyncSession, *, permission_in: PermissionCreate) -> Permission:
    """Cria uma nova Permissão se ela não existir."""
    result = await db.execute(select(Permission).filter(Permission.name == permission_in.name))
    existing_permission = result.scalars().first()
    if existing_permission:
        return existing_permission

    db_permission = Permission(**permission_in.model_dump())
    db.add(db_permission)
    # Nota: O commit será feito no final do script de seed para eficiência
    return db_permission

async def get_permissions(db: AsyncSession, *, skip: int = 0, limit: int = 100) -> List[Permission]:
    """Busca uma lista de todas as Permissões."""
    result = await db.execute(select(Permission).order_by(Permission.id).offset(skip).limit(limit))
    return result.scalars().all()
