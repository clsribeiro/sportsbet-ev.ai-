from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.role import RoleRead, RoleCreate, RoleUpdate, RoleReadWithPermissions, RoleUpdatePermissions
from app.crud import crud_role
from app.db.session import get_db_session
from app.api.deps.current_user import get_current_superuser

router = APIRouter()

@router.get("/{role_id}", response_model=RoleReadWithPermissions, tags=["Admin - Gestão de Planos"])
async def get_role_details(
    *, role_id: int, db: AsyncSession = Depends(get_db_session), current_superuser = Depends(get_current_superuser)
):
    """Obtém os detalhes de um plano específico, incluindo suas permissões."""
    role = await crud_role.get_role_by_id(db=db, role_id=role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Plano não encontrado")
    return role

@router.put("/{role_id}", response_model=RoleRead, tags=["Admin - Gestão de Planos"])
async def update_existing_role(
    *, role_id: int, role_in: RoleUpdate, db: AsyncSession = Depends(get_db_session), current_superuser = Depends(get_current_superuser)
):
    """Atualiza os detalhes de um plano (role)."""
    role = await crud_role.get_role_by_id(db=db, role_id=role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Plano não encontrado")
    if role.name == "admin_full":
        raise HTTPException(status_code=403, detail="O plano de Administrador não pode ser modificado.")
    return await crud_role.update_role(db=db, db_role=role, role_in=role_in)

@router.delete("/{role_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Admin - Gestão de Planos"])
async def delete_existing_role(
    *, role_id: int, db: AsyncSession = Depends(get_db_session), current_superuser = Depends(get_current_superuser)
):
    """Apaga um plano (role)."""
    role = await crud_role.get_role_by_id(db=db, role_id=role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Plano não encontrado")
    if role.name == "admin_full":
        raise HTTPException(status_code=403, detail="O plano de Administrador não pode ser apagado.")
    await crud_role.delete_role(db=db, db_role=role)
    return

@router.put("/{role_id}/permissions", response_model=RoleReadWithPermissions, tags=["Admin - Gestão de Planos"])
async def update_permissions_for_role(
    *, role_id: int, permissions_in: RoleUpdatePermissions, db: AsyncSession = Depends(get_db_session), current_superuser = Depends(get_current_superuser)
):
    """Atualiza a lista de permissões associadas a um plano."""
    role = await crud_role.get_role_by_id(db=db, role_id=role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Plano não encontrado")
    return await crud_role.update_role_permissions(db=db, role=role, permission_ids=permissions_in.permission_ids)

@router.post("/", response_model=RoleRead, status_code=status.HTTP_201_CREATED, tags=["Admin - Gestão de Planos"])
async def create_new_role(
    *, role_in: RoleCreate, db: AsyncSession = Depends(get_db_session), current_superuser = Depends(get_current_superuser)
):
    """Cria um novo plano (role) no sistema."""
    return await crud_role.create_role(db=db, role_in=role_in)

@router.get("/", response_model=List[RoleRead], tags=["Admin - Gestão de Planos"])
async def list_roles(
    db: AsyncSession = Depends(get_db_session), current_superuser = Depends(get_current_superuser)
):
    """Obtém uma lista de todos os planos (roles) no sistema."""
    return await crud_role.get_roles(db=db)
