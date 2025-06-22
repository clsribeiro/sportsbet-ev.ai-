from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional, List # Adicione List
from uuid import UUID
from datetime import datetime

from .role import RoleRead # Importe o schema RoleRead

# --- Schemas Existentes ---
class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str = Field(min_length=8, description="Senha do utilizador, mínimo de 8 caracteres")

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    password: Optional[str] = Field(None, min_length=8, description="Nova senha, se for alterar")
    is_active: Optional[bool] = None

# --- NOVOS SCHEMAS ---
class UserUpdateRoles(BaseModel):
    role_ids: List[int] = Field(..., description="Uma lista completa dos IDs dos planos a serem atribuídos ao utilizador.")

class UserRead(UserBase):
    id: UUID
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

# Novo schema para ler um utilizador com os seus planos (roles)
class UserReadWithRoles(UserRead):
    roles: List[RoleRead] = []
    model_config = ConfigDict(from_attributes=True)
