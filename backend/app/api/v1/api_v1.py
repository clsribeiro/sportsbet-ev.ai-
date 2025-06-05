from fastapi import APIRouter

from app.api.v1.endpoints import users # Importa o router de usuários
from app.api.v1.endpoints import health # Importa o router de health check

api_router_v1 = APIRouter()

# Inclui o router de usuários, definindo um prefixo para ele
api_router_v1.include_router(users.router, prefix="/users", tags=["Usuários"])
# Se você usou "/register" no users.router, o caminho completo seria /api/v1/users/register

# Inclui o router de health check
api_router_v1.include_router(health.router, prefix="/health", tags=["Health Check"]) # Movido para cá
