# Modelos de autenticação existentes
from .user import UserBase, UserCreate, UserUpdate, UserRead, UserInDBBase
from .role import RoleBase, RoleCreate, RoleUpdate, RoleRead, RoleInDBBase
from .permission import PermissionBase, PermissionCreate, PermissionUpdate, PermissionRead, PermissionInDBBase
from .token import Token

# Adicionar os novos esquemas de desporto
from .team import TeamBase, TeamCreate, TeamUpdate, TeamRead
from .game import GameBase, GameCreate, GameUpdate, GameRead
