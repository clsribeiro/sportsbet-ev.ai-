from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importe o router principal da v1 da API
from app.api.v1.api_v1 import api_router_v1

app = FastAPI(
    title="SportsBet +EV AI API",
    description="API para a plataforma SportsBet +EV AI, fornecendo análises esportivas e recomendações.",
    version="0.1.0" # Adicionamos uma versão para nossa API
)

origins = [
    "http://localhost:5173",
    "http://192.168.100.169:5173",
    # Adicione outros aqui, como a URL de produção no futuro
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["Root"])
async def root():
    """
    Endpoint raiz da API.
    """
    return {"message": "Bem-vindo à API SportsBet +EV AI!"}

# Inclua o router principal da v1 com um prefixo global /api/v1
app.include_router(api_router_v1, prefix="/api/v1")

# O endpoint /api/v1/health foi movido para api_router_v1, então não é mais necessário aqui.
