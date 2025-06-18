from fastapi import APIRouter

from app.api.v1.endpoints import users, health, auth
from app.api.v1.endpoints import games # Importa o router de jogos

api_router_v1 = APIRouter()

api_router_v1.include_router(auth.router, prefix="/auth", tags=["Autenticação"])
api_router_v1.include_router(users.router, prefix="/users", tags=["Utilizadores"])
api_router_v1.include_router(health.router, prefix="/health", tags=["Health Check"])
api_router_v1.include_router(games.router, prefix="/games", tags=["Jogos"]) # Adiciona o novo router
