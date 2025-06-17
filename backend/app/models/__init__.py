from app.db.base_class import Base # Importante para que os modelos usem a mesma Base

# Importe os modelos de autenticação existentes
from .user import User, user_role_association_table
from .role import Role, role_permission_association_table
from .permission import Permission
from .user_feature_preference import UserFeaturePreference

# Adicione os novos modelos de desporto
from .team import Team
from .game import Game
