from app.db.base_class import Base # Importante para que os modelos usem a mesma Base

# Importe os modelos e as tabelas de associação para que sejam registrados com Base.metadata
from .user import User, user_role_association_table
from .role import Role, role_permission_association_table
from .permission import Permission
from .user_feature_preference import UserFeaturePreference
# from .system_setting import SystemSetting # Se você criar este modelo no futuro
