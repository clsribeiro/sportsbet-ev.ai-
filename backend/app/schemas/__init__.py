# Modelos de autenticação
from .user import UserBase, UserCreate, UserUpdate, UserRead
from .token import Token

# Modelos de Roles/Planos e Permissões
# Corrigido para importar apenas os schemas que existem em role.py
from .role import RoleBase, RoleCreate, RoleUpdate, RoleRead, RoleReadWithPermissions, RoleUpdatePermissions
from .permission import PermissionBase, PermissionCreate, PermissionUpdate, PermissionRead

# Modelos de Desporto
from .team import TeamBase, TeamCreate, TeamUpdate, TeamRead
from .game import GameBase, GameCreate, GameUpdate, GameRead
from .league import LeagueBase, LeagueCreate, LeagueRead
