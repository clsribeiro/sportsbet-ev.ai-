import enum
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, timezone

from app.db.base_class import Base

class BetStatus(str, enum.Enum):
    PENDING = "pending"
    WON = "won"
    LOST = "lost"
    VOID = "void" # Anulada

class Bet(Base):
    __tablename__ = "bets"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # A quem pertence a aposta
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    # A que jogo se refere (opcional, pode ser uma aposta não ligada a um jogo específico)
    game_id = Column(Integer, ForeignKey("games.id"), nullable=True)

    # Detalhes da aposta
    market_name = Column(String(255), nullable=False, comment="Ex: 'Vencedor do Jogo', 'Mais/Menos 2.5 Golos'")
    selection = Column(String(255), nullable=False, comment="Ex: 'Flamengo', 'Mais de 2.5'")
    odds = Column(Float, nullable=False, comment="As odds (cotação) no momento da aposta")
    stake = Column(Float, nullable=False, comment="O valor apostado (unidades ou monetário)")
    status = Column(SQLAlchemyEnum(BetStatus), nullable=False, default=BetStatus.PENDING)
    
    # Controlo
    placed_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    settled_at = Column(DateTime(timezone=True), nullable=True, comment="Data em que a aposta foi resolvida")

    # Relacionamentos
    owner = relationship("User")
    game = relationship("Game")

    def __repr__(self):
        return f"<Bet(id={self.id}, user_id={self.user_id}, market='{self.market_name}')>"
