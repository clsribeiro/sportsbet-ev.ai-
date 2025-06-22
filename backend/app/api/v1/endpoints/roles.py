from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.role import RoleRead, RoleCreate
from app.crud import crud_role
from app.db.session import get_db_session
from app.api.deps.current_user import get_current_superuser
from app.models.user import User

router = APIRouter()

# --- NOVO ENDPOINT DE CRIAÇÃO ---
@router.post(
    "/", 
    response_model=RoleRead, 
    status_code=status.HTTP_201_CREATED,
    summary="Criar um novo Plano (Role)",
    tags=["Admin - Gestão de Planos"]
)
async def create_new_role(
    *,
    role_in: RoleCreate, # Dados do novo plano vêm do corpo da requisição
    db: AsyncSession = Depends(get_db_session),
    current_superuser: User = Depends(get_current_superuser) # Protege a rota
):
    """
    Cria um novo plano (role) no sistema.
    Se um plano com o mesmo nome técnico já existir, ele não será criado novamente.
    Apenas superutilizadores podem aceder.
    """
    # A nossa função crud_role.create_role já verifica se o role existe,
    # mas podemos adicionar uma verificação explícita aqui para dar uma resposta mais clara se quisermos.
    role = await crud_role.create_role(db=db, role_in=role_in)
    return role

# --- ENDPOINT DE LISTAGEM EXISTENTE ---
@router.get("/", response_model=List[RoleRead], summary="Listar todos os Planos (Roles)", tags=["Admin - Gestão de Planos"])
async def list_roles(
    db: AsyncSession = Depends(get_db_session),
    current_superuser: User = Depends(get_current_superuser),
):
    """
    Obtém uma lista de todos os planos (roles) no sistema.
    Apenas superutilizadores podem aceder.
    """
    roles = await crud_role.get_roles(db=db)
    return roles
