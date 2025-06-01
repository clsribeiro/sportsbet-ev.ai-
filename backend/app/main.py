from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importe o router do health check
from app.api.v1.endpoints import health  # Assumindo que __init__.py estão nos lugares certos

app = FastAPI(title="SportsBet +EV AI API") # Adicionamos um título à nossa API

# Lista de origens permitidas (endereços do seu frontend)
origins = [
    "http://localhost:5173",
    "http://192.168.100.169:5173", # IP da sua VM na rede local
    # Adicione outros endereços de frontend aqui se necessário
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Bem-vindo à API SportsBet +EV AI!"}

# Inclua o router do health check com um prefixo para a v1 da API
app.include_router(health.router, prefix="/api/v1", tags=["Health Check"])

# Outros routers da v1 podem ser adicionados aqui
