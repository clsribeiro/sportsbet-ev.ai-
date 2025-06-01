from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime

# Esquema base com campos comuns, pode ser herdado por outros
class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None

# Esquema para criação de usuário (o que a API espera no POST)
class UserCreate(UserBase):
    password: str = Field(min_length=8, description="Senha do usuário, mínimo de 8 caracteres")

# Esquema para atualizar usuário (nem todos os campos são obrigatórios na atualização)
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    password: Optional[str] = Field(None, min_length=8, description="Nova senha, se for alterar")
    is_active: Optional[bool] = None
    # is_superuser só deve ser alterado por outro superuser, em um endpoint específico
    # is_superuser: Optional[bool] = None

# Esquema para representar o usuário como ele existe no banco de dados (inclui hashed_password)
# Este geralmente não é exposto diretamente na API para leitura de dados do usuário.
class UserInDBBase(UserBase):
    id: UUID = Field(default_factory=uuid4)
    hashed_password: str
    is_active: bool = True
    is_superuser: bool = False
    created_at: datetime = Field(default_factory=datetime.now) # Usar datetime.utcnow se preferir UTC
    updated_at: datetime = Field(default_factory=datetime.now) # Usar datetime.utcnow se preferir UTC

    # Configuração para Pydantic v2 para permitir criação a partir de atributos de objeto (ex: ORM)
    model_config = ConfigDict(from_attributes=True)

# Esquema para ler/retornar dados do usuário na API (NÃO inclui hashed_password)
class UserRead(UserBase):
    id: UUID
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: datetime

    # Configuração para Pydantic v2
    model_config = ConfigDict(from_attributes=True)
