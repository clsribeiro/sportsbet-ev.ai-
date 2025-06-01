from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from uuid import UUID # Se Permissions tiverem IDs UUID, ou para outros links no futuro
# Para os IDs de Role e Permission, vamos usar int conforme planejado.

# Esquema base para Role/Plano
class RoleBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=50, description="Nome técnico do papel/plano (ex: plan_starter)")
    display_name: str = Field(..., min_length=3, max_length=100, description="Nome amigável do papel/plano (ex: +EV Starter)")
    description: Optional[str] = Field(None, max_length=255, description="Descrição do papel/plano")
    is_active: bool = True

# Esquema para criar um novo Role/Plano
class RoleCreate(RoleBase):
    pass # Herda todos os campos de RoleBase, pode adicionar mais se necessário

# Esquema para atualizar um Role/Plano
class RoleUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=50)
    display_name: Optional[str] = Field(None, min_length=3, max_length=100)
    description: Optional[str] = Field(None, max_length=255)
    is_active: Optional[bool] = None
    # price_monthly: Optional[float] = None # Campos de preço podem ser adicionados aqui
    # price_yearly: Optional[float] = None
    # sort_order: Optional[int] = None

# Esquema para representar o Role/Plano como está no DB
class RoleInDBBase(RoleBase):
    id: int
    # created_at: datetime # Poderíamos adicionar timestamps se necessário
    # updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

# Esquema para ler/retornar dados do Role/Plano na API
# Poderia incluir a lista de permissões associadas, mas faremos isso em um schema mais completo depois
class RoleRead(RoleBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
