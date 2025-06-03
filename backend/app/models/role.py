from sqlalchemy import Column, Integer, String, Boolean, Text, Table, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from app.db.base_class import Base
# Importar a tabela de associação de user.py para o back_populates
from .user import user_role_association_table

# Tabela de associação para a relação muitos-para-muitos entre Role e Permission
role_permission_association_table = Table(
    "role_permission_association", # Nome da tabela de associação
    Base.metadata,
    Column("role_id", Integer, ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True),
    Column("permission_id", Integer, ForeignKey("permissions.id", ondelete="CASCADE"), primary_key=True),
)

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(50), unique=True, index=True, nullable=False)
    display_name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    # Opcional: adicionar timestamps se quiser rastrear quando roles são criados/modificados
    # created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    # updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relacionamento com User (muitos-para-muitos)
    users = relationship(
        "User",
        secondary=user_role_association_table, # Usa a tabela importada de user.py
        back_populates="roles"
    )

    # Relacionamento com Permission (muitos-para-muitos)
    permissions = relationship(
        "Permission",
        secondary=role_permission_association_table,
        back_populates="roles",
        lazy="selectin" # 'selectin' é uma estratégia de carregamento eficiente para muitos-para-muitos
    )

    def __repr__(self):
        return f"<Role(id={self.id}, name='{self.name}')>"
