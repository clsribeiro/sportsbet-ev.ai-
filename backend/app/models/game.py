from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum as SQLAlchemyEnum, Text # Adicione Text
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import enum

from app.db.base_class import Base

class GameStatus(str, enum.Enum):
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    FINISHED = "finished"
    POSTPONED = "postponed"
    CANCELLED = "cancelled"

class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    home_team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    away_team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)

    game_time = Column(DateTime(timezone=True), nullable=False, index=True)
    status = Column(SQLAlchemyEnum(GameStatus), nullable=False, default=GameStatus.SCHEDULED)

    home_score = Column(Integer, nullable=True)
    away_score = Column(Integer, nullable=True)

    # --- NOVOS CAMPOS ADICIONADOS ---
    analysis = Column(Text, nullable=True, comment="Análise descritiva e o que esperar do jogo.")
    value_bet_tip = Column(Text, nullable=True, comment="Dica de aposta de valor (+EV) identificada.")
    # --- FIM DOS NOVOS CAMPOS ---

    api_provider = Column(String(50), nullable=True)
    api_game_id = Column(String(100), nullable=True)

    home_team = relationship("Team", back_populates="home_games", foreign_keys=[home_team_id])
    away_team = relationship("Team", back_populates="away_games", foreign_keys=[away_team_id])

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<Game(id={self.id}, home_team_id={self.home_team_id}, away_team_id={self.away_team_id})>"
