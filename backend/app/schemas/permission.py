from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

# Esquema base para Permissão
class PermissionBase(BaseModel):
    name: str = Field(..., min_length=5, max_length=100, description="Nome técnico da permissão (ex: feature:view_game_schedule)")
    description: Optional[str] = Field(None, max_length=255, description="Descrição da permissão")
    module_group: Optional[str] = Field(None, max_length=50, description="Grupo do módulo para organização (ex: Visualização de Dados)")

# Esquema para criar uma nova Permissão
class PermissionCreate(PermissionBase):
    pass

# Esquema para atualizar uma Permissão
class PermissionUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=5, max_length=100)
    description: Optional[str] = Field(None, max_length=255)
    module_group: Optional[str] = Field(None, max_length=50)

# Esquema para ler/retornar dados da Permissão na API
class PermissionRead(PermissionBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
