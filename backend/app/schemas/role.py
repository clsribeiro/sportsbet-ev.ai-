from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List

# Importar o schema de permissão para o relacionamento
from .permission import PermissionRead 

# --- Esquemas para Role ---

# Esquema base com os campos principais de um Role/Plano
class RoleBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=50, description="Nome técnico do papel/plano (ex: plan_starter)")
    display_name: str = Field(..., min_length=3, max_length=100, description="Nome amigável do papel/plano (ex: +EV Starter)")
    description: Optional[str] = Field(None, max_length=255, description="Descrição do papel/plano")
    is_active: bool = True

# Esquema usado para criar um novo Role/Plano
class RoleCreate(RoleBase):
    pass

# Esquema usado para atualizar os dados de um Role/Plano
class RoleUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=50)
    display_name: Optional[str] = Field(None, min_length=3, max_length=100)
    description: Optional[str] = Field(None, max_length=255)
    is_active: Optional[bool] = None

# Esquema para receber a lista de IDs de permissões para atualizar
class RoleUpdatePermissions(BaseModel):
    permission_ids: List[int]

# Esquema para ler/retornar dados de um Role da API (versão simples)
class RoleRead(RoleBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

# NOVO ESQUEMA: para ler/retornar um Role com as suas permissões
class RoleReadWithPermissions(RoleRead):
    permissions: List[PermissionRead] = [] # Inclui uma lista de permissões
    model_config = ConfigDict(from_attributes=True)