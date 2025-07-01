from app.db.base_class import Base

# Modelos de autenticação
from .user import User, user_role_association_table
from .role import Role, role_permission_association_table
from .permission import Permission
from .user_feature_preference import UserFeaturePreference

# Modelos de desporto
from .team import Team
from .game import Game, GameStatus
from .league import League
from .prediction import Prediction

# Novo modelo de aposta
from .bet import Bet, BetStatus
