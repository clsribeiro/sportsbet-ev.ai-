from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.user import UserReadWithRoles, UserUpdateRoles
from app.crud import crud_user
from app.db.session import get_db_session
from app.api.deps.current_user import get_current_superuser
from app.models.user import User

router = APIRouter()

@router.get(
    "/",
    response_model=List[UserReadWithRoles],
    summary="Listar todos os Utilizadores",
    tags=["Admin - Gestão de Utilizadores"]
)
async def list_users(
    db: AsyncSession = Depends(get_db_session),
    current_superuser: User = Depends(get_current_superuser),
):
    """Obtém uma lista de todos os utilizadores no sistema."""
    users = await crud_user.get_users(db=db)
    return users

@router.put(
    "/{user_id}/roles",
    response_model=UserReadWithRoles,
    summary="Atualizar os Planos de um Utilizador",
    tags=["Admin - Gestão de Utilizadores"]
)
async def update_user_roles_by_admin(
    *,
    user_id: UUID,
    roles_in: UserUpdateRoles,
    db: AsyncSession = Depends(get_db_session),
    current_superuser: User = Depends(get_current_superuser),
):
    """Atualiza a lista de planos (roles) associados a um utilizador."""
    user = await crud_user.get_user_by_id(db=db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Utilizador não encontrado")

    updated_user = await crud_user.update_user_roles(
        db=db, user=user, role_ids=roles_in.role_ids
    )
    return updated_user
