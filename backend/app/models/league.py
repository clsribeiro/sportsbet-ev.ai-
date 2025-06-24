from sqlalchemy import Column, Integer, String, Boolean
from app.db.base_class import Base

class League(Base):
    __tablename__ = "leagues"

    id = Column(Integer, primary_key=True, comment="O ID da liga na API-Futebol")
    name = Column(String(100), nullable=False, index=True)
    country = Column(String(100), nullable=False)
    logo = Column(String(255), nullable=True)
    type = Column(String(50), nullable=True) # Ex: League, Cup
    is_sync_enabled = Column(Boolean, default=False, nullable=False, comment="Flag para controlar se sincronizamos equipas e jogos desta liga")

    def __repr__(self):
        return f"<League(id={self.id}, name='{self.name}')>"
