from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime
from uuid import UUID

from app.models.bet import BetStatus

class BetBase(BaseModel):
    game_id: Optional[int] = None
    market_name: str = Field(..., max_length=255)
    selection: str = Field(..., max_length=255)
    odds: float = Field(..., gt=1.0, description="As odds devem ser maiores que 1.0")
    stake: float = Field(..., gt=0, description="O valor apostado deve ser positivo")
    status: BetStatus = BetStatus.PENDING

class BetCreate(BetBase):
    pass # O user_id será obtido do utilizador autenticado

class BetUpdate(BaseModel):
    status: BetStatus

class BetRead(BetBase):
    id: int
    user_id: UUID
    placed_at: datetime
    settled_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)
