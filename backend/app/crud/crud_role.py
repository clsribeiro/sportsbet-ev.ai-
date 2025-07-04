from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from typing import List

from app.models.role import Role
from app.models.permission import Permission
from app.schemas.role import RoleCreate, RoleUpdate

async def get_role_by_id(db: AsyncSession, *, role_id: int) -> Role | None:
    """Busca um único Role pelo seu ID, carregando as permissões relacionadas."""
    result = await db.execute(
        select(Role).where(Role.id == role_id).options(selectinload(Role.permissions))
    )
    return result.scalars().first()

async def update_role(db: AsyncSession, *, db_role: Role, role_in: RoleUpdate) -> Role:
    """Atualiza os dados de um Role."""
    update_data = role_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_role, field, value)
    db.add(db_role)
    await db.commit()
    await db.refresh(db_role)
    return db_role

async def delete_role(db: AsyncSession, *, db_role: Role) -> None:
    """Apaga um Role do banco de dados."""
    await db.delete(db_role)
    await db.commit()
    return

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

async def update_role_permissions(db: AsyncSession, *, role: Role, permission_ids: List[int]) -> Role:
    """Atualiza as permissões de um Role."""
    result = await db.execute(select(Permission).where(Permission.id.in_(permission_ids)))
    role.permissions = result.scalars().all()
    db.add(role)
    await db.commit()
    await db.refresh(role)
    # Recarrega o role com as permissões para a resposta
    return await get_role_by_id(db, role_id=role.id)
