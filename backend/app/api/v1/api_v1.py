from fastapi import APIRouter

# Importa todos os routers que vamos usar
from app.api.v1.endpoints import users, health, auth, games, roles, permissions
from app.api.v1.endpoints import admin_users # <- ESTA ERA A IMPORTAÇÃO QUE FALTAVA
from app.api.v1.endpoints import predictions, admin_tasks # Importa os novos routers

api_router_v1 = APIRouter()

# Rotas Públicas/Padrão
api_router_v1.include_router(auth.router, prefix="/auth", tags=["Autenticação"])
api_router_v1.include_router(users.router, prefix="/users", tags=["Utilizadores"])
api_router_v1.include_router(health.router, prefix="/health", tags=["Health Check"])
api_router_v1.include_router(games.router, prefix="/games", tags=["Jogos"])
api_router_v1.include_router(predictions.router, prefix="/predictions", tags=["Previsões"]) # Adiciona o router de previsões

# Rotas de Administração
api_router_v1.include_router(roles.router, prefix="/admin/roles", tags=["Admin - Gestão de Planos"])
api_router_v1.include_router(permissions.router, prefix="/admin/permissions", tags=["Admin - Gestão de Permissões"])
api_router_v1.include_router(admin_users.router, prefix="/admin/users", tags=["Admin - Gestão de Utilizadores"])

# Rotas de Administração
# ... (include_router existentes para admin/roles, admin/permissions, admin/users)
api_router_v1.include_router(admin_tasks.router, prefix="/admin/tasks", tags=["Admin - Tarefas"]) # Adiciona o router de tarefas de admin