from pydantic import BaseModel, Field
from typing import Optional

# Novo schema para o admin atualizar os dados de um utilizador
class AdminUserUpdate(BaseModel):
    full_name: Optional[str] = None
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None

# Novo schema para o admin redefinir a senha de um utilizador
class AdminPasswordUpdate(BaseModel):
    new_password: str = Field(..., min_length=8, description="Nova senha, mínimo de 8 caracteres")
