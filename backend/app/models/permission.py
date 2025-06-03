from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from app.db.base_class import Base
# Importar a tabela de associação de role.py para o back_populates
from .role import role_permission_association_table

class Permission(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), unique=True, index=True, nullable=False) # Ex: feature:view_game_schedule
    description = Column(Text, nullable=True)
    module_group = Column(String(50), nullable=True) # Ex: Visualização de Dados
    # Opcional: adicionar timestamps
    # created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    # updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relacionamento com Role (muitos-para-muitos)
    roles = relationship(
        "Role",
        secondary=role_permission_association_table, # Usa a tabela importada de role.py
        back_populates="permissions"
    )

    def __repr__(self):
        return f"<Permission(id={self.id}, name='{self.name}')>"
