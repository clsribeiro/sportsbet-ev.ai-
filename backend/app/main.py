from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.api_v1 import api_router_v1
from app.api.v1.endpoints import websockets

app = FastAPI(
    title="SportsBet +EV AI API",
    description="API para a plataforma SportsBet +EV AI.",
    version="0.1.0"
)

origins = [
    "http://localhost:5173",
    "http://192.168.100.169:5173",
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
    """Endpoint raiz da API."""
    return {"message": "Bem-vindo à API SportsBet +EV AI!"}

app.include_router(api_router_v1, prefix="/api/v1")
app.include_router(websockets.router)
