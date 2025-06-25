from sqlalchemy import Column, Integer, String, Text, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from app.db.base_class import Base

class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    game_id = Column(Integer, ForeignKey("games.id", ondelete="CASCADE"), unique=True, nullable=False)

    # A previsão gerada pela IA
    predicted_winner = Column(String(100), nullable=True, comment="Nome da equipa prevista para vencer")
    prediction_summary = Column(Text, nullable=True, comment="Um resumo da análise da IA")
    value_bet_suggestion = Column(Text, nullable=True, comment="A dica de aposta de valor específica")

    # Dados numéricos da previsão
    home_win_probability = Column(Float, nullable=True)
    away_win_probability = Column(Float, nullable=True)
    draw_probability = Column(Float, nullable=True)

    confidence_level = Column(Float, nullable=True, comment="Nível de confiança da IA na previsão (0.0 a 1.0)")

    # Controlo
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    model_version = Column(String(50), nullable=True, comment="Versão do modelo de IA ou prompt usado")

    # Relacionamento com o jogo
    game = relationship("Game")

    def __repr__(self):
        return f"<Prediction(id={self.id}, game_id={self.game_id})>"
