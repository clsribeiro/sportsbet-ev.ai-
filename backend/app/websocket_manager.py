import asyncio
import json
from fastapi import WebSocket
from typing import Dict
from uuid import UUID

class ConnectionManager:
    """Gere as conexões WebSocket ativas."""
    def __init__(self):
        self.active_connections: Dict[UUID, WebSocket] = {}

    async def connect(self, websocket: WebSocket, user_id: UUID):
        """Associa uma conexão WebSocket já aceite a um ID de utilizador."""
        self.active_connections[user_id] = websocket
        print(f"Conexão associada ao utilizador: {user_id}. Total de conexões: {len(self.active_connections)}")

    def disconnect(self, user_id: UUID):
        """Remove uma conexão WebSocket pelo ID do utilizador."""
        if user_id in self.active_connections:
            del self.active_connections[user_id]
            print(f"Cliente desconectado: {user_id}. Total de conexões: {len(self.active_connections)}")

    async def broadcast(self, message_text: str):
        """Envia uma mensagem de texto para todos os utilizadores conectados."""
        if not self.active_connections:
            return

        payload = {"type": "notification", "message": message_text}
        message = json.dumps(payload)
        
        tasks = [
            connection.send_text(message)
            for connection in self.active_connections.values()
        ]
        if tasks:
            await asyncio.gather(*tasks)

manager = ConnectionManager()
