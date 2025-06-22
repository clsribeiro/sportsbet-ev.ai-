from fastapi import APIRouter

from app.api.v1.endpoints import users, health, auth
from app.api.v1.endpoints import games # Importa o router de jogos
from app.api.v1.endpoints import roles, permissions # Importa os novos routers

api_router_v1 = APIRouter()

api_router_v1.include_router(auth.router, prefix="/auth", tags=["Autenticação"])
api_router_v1.include_router(users.router, prefix="/users", tags=["Utilizadores"])
api_router_v1.include_router(health.router, prefix="/health", tags=["Health Check"])
api_router_v1.include_router(games.router, prefix="/games", tags=["Jogos"]) # Adiciona o novo router
# Adiciona os novos routers de admin
api_router_v1.include_router(roles.router, prefix="/admin/roles", tags=["Admin - Gestão de Planos"])
api_router_v1.include_router(permissions.router, prefix="/admin/permissions", tags=["Admin - Gestão de Permissões"])
