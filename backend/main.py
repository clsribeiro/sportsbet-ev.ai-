from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware # Importe o CORSMiddleware

app = FastAPI()

# Lista de origens permitidas (endereços do seu frontend)
origins = [
    "http://localhost:5173",          # Endereço do Vite ao rodar localmente na VM
    "http://192.168.100.169:5173",    # Endereço do Vite na sua rede local (seu IP da VM)
    # Adicione aqui outros endereços se necessário (ex: endereço de produção no futuro)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Permite as origens listadas
    allow_credentials=True, # Permite cookies (útil para autenticação no futuro)
    allow_methods=["*"],    # Permite todos os métodos HTTP (GET, POST, etc.)
    allow_headers=["*"],    # Permite todos os cabeçalhos HTTP
)

@app.get("/")
async def root():
    return {"message": "Olá Mundo do Backend SportsBet +EV AI!"}

@app.get("/api/health")
async def health_check():
    return {"status": "Backend saudável e operante!"}
