from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class LeagueBase(BaseModel):
    id: int
    name: str
    country: str
    logo: Optional[str] = None
    type: Optional[str] = None

class LeagueCreate(LeagueBase):
    pass

class LeagueRead(LeagueBase):
    is_sync_enabled: bool
    model_config = ConfigDict(from_attributes=True)
