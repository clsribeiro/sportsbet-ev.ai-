from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional, List
from uuid import UUID
from datetime import datetime
from .role import RoleRead

# --- Schemas para User ---

class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str = Field(min_length=8)

class UserUpdate(BaseModel):
    # Apenas os campos que um utilizador pode atualizar no seu perfil
    full_name: Optional[str] = None

# NOVO SCHEMA: Para o formulário de alteração de senha
class UserPasswordUpdate(BaseModel):
    current_password: str
    new_password: str = Field(min_length=8)

class UserUpdateRoles(BaseModel):
    role_ids: List[int]

class UserRead(UserBase):
    id: UUID
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

class UserReadWithRoles(UserRead):
    roles: List[RoleRead] = []
    model_config = ConfigDict(from_attributes=True)
