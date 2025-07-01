# Modelos de autenticação
from .user import UserBase, UserCreate, UserUpdate, UserRead, UserReadWithRoles, UserUpdateRoles, UserPasswordUpdate
from .token import Token

# Modelos de Roles/Planos e Permissões
from .role import RoleBase, RoleCreate, RoleUpdate, RoleRead, RoleReadWithPermissions, RoleUpdatePermissions
from .permission import PermissionBase, PermissionCreate, PermissionUpdate, PermissionRead

# Modelos de Desporto
from .team import TeamBase, TeamCreate, TeamUpdate, TeamRead
from .game import GameBase, GameCreate, GameUpdate, GameRead
from .league import LeagueBase, LeagueCreate, LeagueRead

# Modelos de Previsão
from .prediction import PredictionBase, PredictionCreate, PredictionRead, PredictionReadWithGame

# Novos schemas de aposta
from .bet import BetBase, BetCreate, BetUpdate, BetRead
