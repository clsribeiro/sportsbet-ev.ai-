from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from app.models.permission import Permission

async def get_permissions(db: AsyncSession, *, skip: int = 0, limit: int = 100) -> List[Permission]:
    """Busca uma lista de todas as Permissões."""
    result = await db.execute(select(Permission).order_by(Permission.id).offset(skip).limit(limit))
    return result.scalars().all()
