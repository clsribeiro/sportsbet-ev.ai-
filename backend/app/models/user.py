from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID # Para ID do tipo UUID no PostgreSQL
import uuid # Para gerar UUIDs
from datetime import datetime, timezone # Importar timezone

from app.db.base_class import Base # Importe sua Base declarativa

# Tabela de associação para a relação muitos-para-muitos entre User e Role
# Definida aqui para que User e Role possam referenciá-la.
user_role_association_table = Table(
    "user_role_association", # Nome da tabela de associação
    Base.metadata,
    Column("user_id", UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    Column("role_id", Integer, ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True),
)

class User(Base):
    __tablename__ = "users" # Nome da tabela no banco de dados

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(100), index=True, nullable=True)
    is_active = Column(Boolean(), default=True, nullable=False)
    is_superuser = Column(Boolean(), default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relacionamento com Role (muitos-para-muitos)
    roles = relationship(
        "Role", # Nome da classe do modelo relacionado
        secondary=user_role_association_table,
        back_populates="users"
    )

    # Relacionamento com UserFeaturePreference (um-para-muitos)
    feature_preferences = relationship(
        "UserFeaturePreference",
        back_populates="user",
        cascade="all, delete-orphan" # Se um User for deletado, suas preferências também serão
    )

    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}')>"
