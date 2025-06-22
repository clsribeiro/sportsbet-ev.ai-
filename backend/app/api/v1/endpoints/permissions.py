from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.permission import PermissionRead
from app.crud import crud_permission
from app.db.session import get_db_session
from app.api.deps.current_user import get_current_superuser
from app.models.user import User

router = APIRouter()

@router.get("/", response_model=List[PermissionRead], summary="Listar todas as Permissões", tags=["Admin - Gestão de Permissões"])
async def list_permissions(
    db: AsyncSession = Depends(get_db_session),
    current_superuser: User = Depends(get_current_superuser), # Protege a rota
):
    """
    Obtém uma lista de todas as permissões disponíveis no sistema.
    Apenas superutilizadores podem aceder.
    """
    permissions = await crud_permission.get_permissions(db=db)
    return permissions
