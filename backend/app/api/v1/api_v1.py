from fastapi import APIRouter
from app.api.v1.endpoints import users # Importa o router de usuários
from app.api.v1.endpoints import health # Importa o router de health check
from app.api.v1.endpoints import auth # Importa o novo router
api_router_v1 = APIRouter()
api_router_v1.include_router(auth.router, prefix="/auth", tags=["Autenticação"]) # Adiciona o router de auth
api_router_v1.include_router(users.router, prefix="/users", tags=["Usuários"])
api_router_v1.include_router(health.router, prefix="/health", tags=["Health Check"])
