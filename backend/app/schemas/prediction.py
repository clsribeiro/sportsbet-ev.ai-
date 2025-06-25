from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime

class PredictionBase(BaseModel):
    predicted_winner: Optional[str] = None
    prediction_summary: Optional[str] = None
    value_bet_suggestion: Optional[str] = None
    home_win_probability: Optional[float] = Field(None, ge=0, le=1)
    away_win_probability: Optional[float] = Field(None, ge=0, le=1)
    draw_probability: Optional[float] = Field(None, ge=0, le=1)
    confidence_level: Optional[float] = Field(None, ge=0, le=1)
    model_version: Optional[str] = None

class PredictionCreate(PredictionBase):
    game_id: int

class PredictionRead(PredictionBase):
    id: int
    game_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
