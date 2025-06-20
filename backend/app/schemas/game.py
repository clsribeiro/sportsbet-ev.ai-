from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime

from app.models.game import GameStatus
from .team import TeamRead

# --- Esquemas para Game ---

class GameBase(BaseModel):
    home_team_id: int
    away_team_id: int
    game_time: datetime
    status: GameStatus = GameStatus.SCHEDULED

class GameCreate(GameBase):
    pass

# Esquema usado para atualizar um jogo
class GameUpdate(BaseModel):
    status: Optional[GameStatus] = None
    home_score: Optional[int] = None
    away_score: Optional[int] = None
    game_time: Optional[datetime] = None
    # --- NOVOS CAMPOS ADICIONADOS ---
    analysis: Optional[str] = None
    value_bet_tip: Optional[str] = None
    # --- FIM DOS NOVOS CAMPOS ---

# Esquema usado para retornar os dados de um jogo da API
class GameRead(GameBase):
    id: int
    home_score: Optional[int] = None
    away_score: Optional[int] = None
    # --- NOVOS CAMPOS ADICIONADOS ---
    analysis: Optional[str] = None
    value_bet_tip: Optional[str] = None
    # --- FIM DOS NOVOS CAMPOS ---

    home_team: TeamRead
    away_team: TeamRead

    model_config = ConfigDict(from_attributes=True)
