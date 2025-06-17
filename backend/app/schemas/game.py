from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime

# Importar o enum de status do nosso modelo SQLAlchemy e o schema TeamRead
from app.models.game import GameStatus
from .team import TeamRead

# --- Esquemas para Game ---

# Esquema base com os campos principais de um jogo
class GameBase(BaseModel):
    home_team_id: int
    away_team_id: int
    game_time: datetime
    status: GameStatus = GameStatus.SCHEDULED

# Esquema usado para criar um novo jogo
class GameCreate(GameBase):
    pass # Herda todos os campos

# Esquema usado para atualizar um jogo (ex: atualizar o status e o resultado)
class GameUpdate(BaseModel):
    status: Optional[GameStatus] = None
    home_score: Optional[int] = None
    away_score: Optional[int] = None
    game_time: Optional[datetime] = None

# Esquema usado para retornar os dados de um jogo da API
class GameRead(GameBase):
    id: int
    home_score: Optional[int] = None
    away_score: Optional[int] = None

    # Campos de relacionamento para exibir os dados completos das equipas
    # Isto permite que a resposta JSON contenha objetos completos das equipas.
    home_team: TeamRead
    away_team: TeamRead

    model_config = ConfigDict(from_attributes=True)
