from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.role import RoleRead
from app.crud import crud_role
from app.db.session import get_db_session
from app.api.deps.current_user import get_current_superuser
from app.models.user import User

router = APIRouter()

@router.get("/", response_model=List[RoleRead], summary="Listar todos os Planos (Roles)", tags=["Admin - Gestão de Planos"])
async def list_roles(
    db: AsyncSession = Depends(get_db_session),
    current_superuser: User = Depends(get_current_superuser), # Protege a rota
):
    """
    Obtém uma lista de todos os planos (roles) no sistema.
    Apenas superutilizadores podem aceder.
    """
    roles = await crud_role.get_roles(db=db)
    return roles
