from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from typing import List

from app.models.role import Role
from app.models.permission import Permission # Importar Permission
from app.schemas.role import RoleCreate

async def get_role_by_id(db: AsyncSession, *, role_id: int) -> Role | None:
    """Busca um único Role pelo seu ID, carregando as permissões relacionadas."""
    result = await db.execute(
        select(Role)
        .where(Role.id == role_id)
        .options(selectinload(Role.permissions)) # Carregamento otimizado das permissões
    )
    return result.scalars().first()

async def update_role_permissions(db: AsyncSession, *, role: Role, permission_ids: List[int]) -> Role:
    """Atualiza as permissões de um Role."""
    # Busca todos os objetos de permissão correspondentes aos IDs fornecidos
    result = await db.execute(select(Permission).where(Permission.id.in_(permission_ids)))
    permissions = result.scalars().all()

    # Substitui a lista de permissões do role pela nova lista
    role.permissions = permissions

    db.add(role)
    await db.commit()
    await db.refresh(role)

    # Recarrega o role com as permissões para a resposta
    updated_role = await get_role_by_id(db, role_id=role.id)
    return updated_role

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