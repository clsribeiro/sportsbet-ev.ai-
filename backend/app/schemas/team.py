from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

# --- Esquemas para Team ---

# Esquema base com os campos principais de uma equipa
class TeamBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, description="Nome completo da equipa")
    sport: str = Field(..., max_length=50, description="Desporto principal (ex: futebol, nba, nfl)")
    league: Optional[str] = Field(None, max_length=100, description="Liga principal onde a equipa compete")
    logo_url: Optional[str] = Field(None, max_length=255, description="URL para o logo da equipa")

# Esquema usado para criar uma nova equipa na base de dados
class TeamCreate(TeamBase):
    pass  # Por enquanto, herda todos os campos da base

# Esquema usado para atualizar os dados de uma equipa
class TeamUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    sport: Optional[str] = Field(None, max_length=50)
    league: Optional[str] = Field(None, max_length=100)
    logo_url: Optional[str] = Field(None, max_length=255)

# Esquema usado para retornar os dados de uma equipa da API
class TeamRead(TeamBase):
    id: int

    # Configuração para Pydantic v2 para permitir a criação do esquema a partir de um objeto ORM
    model_config = ConfigDict(from_attributes=True)
