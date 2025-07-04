from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.user import UserReadWithRoles, UserUpdateRoles
from app.schemas.admin import AdminUserUpdate, AdminPasswordUpdate
from app.crud import crud_user
from app.db.session import get_db_session
from app.api.deps.current_user import get_current_superuser
from app.models.user import User

router = APIRouter()

@router.get("/", response_model=List[UserReadWithRoles], tags=["Admin - Gestão de Utilizadores"])
async def list_users(
    db: AsyncSession = Depends(get_db_session), current_superuser: User = Depends(get_current_superuser)
):
    """Obtém uma lista de todos os utilizadores no sistema."""
    return await crud_user.get_users(db=db)

# --- NOVO ENDPOINT ---
@router.get("/{user_id}", response_model=UserReadWithRoles, tags=["Admin - Gestão de Utilizadores"])
async def get_user_by_id_by_admin(
    *, user_id: UUID, db: AsyncSession = Depends(get_db_session), current_superuser: User = Depends(get_current_superuser)
):
    """Busca os detalhes de um utilizador específico, incluindo os seus planos (roles)."""
    user = await crud_user.get_user_by_id_with_permissions(db=db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Utilizador não encontrado")
    return user

@router.put("/{user_id}/roles", response_model=UserReadWithRoles, tags=["Admin - Gestão de Utilizadores"])
async def update_user_roles_by_admin(
    *, user_id: UUID, roles_in: UserUpdateRoles, db: AsyncSession = Depends(get_db_session), current_superuser: User = Depends(get_current_superuser)
):
    """Atualiza a lista de planos (roles) associados a um utilizador."""
    user = await crud_user.get_user_by_id_with_permissions(db=db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Utilizador não encontrado")
    return await crud_user.update_user_roles(db=db, user=user, role_ids=roles_in.role_ids)

@router.put("/{user_id}", response_model=UserReadWithRoles, tags=["Admin - Gestão de Utilizadores"])
async def update_user_by_admin(
    *, user_id: UUID, user_in: AdminUserUpdate, db: AsyncSession = Depends(get_db_session), current_superuser: User = Depends(get_current_superuser)
):
    """Atualiza os detalhes de um utilizador (nome, status)."""
    user = await crud_user.get_user_by_id_with_permissions(db=db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Utilizador não encontrado")
    return await crud_user.update_user(db=db, db_user=user, user_in=user_in)

@router.post("/{user_id}/password-reset", status_code=status.HTTP_204_NO_CONTENT, tags=["Admin - Gestão de Utilizadores"])
async def reset_user_password_by_admin(
    *, user_id: UUID, password_in: AdminPasswordUpdate, db: AsyncSession = Depends(get_db_session), current_superuser: User = Depends(get_current_superuser)
):
    """Redefine a senha de um utilizador."""
    user = await crud_user.get_user_by_id(db=db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Utilizador não encontrado")
    await crud_user.update_user(db=db, db_user=user, user_in={"password": password_in.new_password})
    return
