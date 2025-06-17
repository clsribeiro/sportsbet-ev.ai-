from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship

from app.db.base_class import Base

class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    sport = Column(String(50), nullable=False, index=True) # Ex: "futebol", "nba", "nfl"
    league = Column(String(100), nullable=True, index=True) # Ex: "Brasileirão Série A", "NBA", "NFL"
    logo_url = Column(String(255), nullable=True) # URL para o logo da equipa

    # Relacionamentos para jogos em casa e fora
    home_games = relationship("Game", back_populates="home_team", foreign_keys="[Game.home_team_id]")
    away_games = relationship("Game", back_populates="away_team", foreign_keys="[Game.away_team_id]")

    def __repr__(self):
        return f"<Team(id={self.id}, name='{self.name}')>"
