from sqlalchemy import Column, Integer, Boolean, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.schema import UniqueConstraint
from datetime import datetime, timezone

from app.db.base_class import Base

class UserFeaturePreference(Base):
    __tablename__ = "user_feature_preferences"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    permission_id = Column(Integer, ForeignKey("permissions.id", ondelete="CASCADE"), nullable=False) # Liga à permissão que está sendo habilitada/desabilitada
    is_enabled_by_user = Column(Boolean, default=True, nullable=False)
    # Opcional: adicionar timestamps
    # created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    # updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))


    # Relacionamentos
    user = relationship("User", back_populates="feature_preferences")
    permission = relationship("Permission") # Relacionamento simples, apenas para buscar a permissão se necessário

    # Garante que um usuário só pode ter uma preferência por permissão
    __table_args__ = (UniqueConstraint('user_id', 'permission_id', name='_user_permission_preference_uc'),)

    def __repr__(self):
        return f"<UserFeaturePreference(user_id={self.user_id}, permission_id={self.permission_id}, enabled={self.is_enabled_by_user})>"
