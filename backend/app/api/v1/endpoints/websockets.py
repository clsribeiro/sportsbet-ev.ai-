import json
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db_session
from app.websocket_manager import manager
from app.api.deps.current_user import _get_user_from_token

router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    db: AsyncSession = Depends(get_db_session)
):
    """Endpoint WebSocket com autenticação pós-conexão."""
    await websocket.accept()
    user_id = None
    try:
        auth_data_str = await websocket.receive_text()
        auth_data = json.loads(auth_data_str)
        token = auth_data.get("token")
        
        if auth_data.get("type") == "auth" and token:
            user = await _get_user_from_token(token=token, db=db)
            if user:
                user_id = user.id
                await manager.connect(websocket, user_id)
                await websocket.send_json({"type": "auth_success", "message": "Conectado ao servidor de alertas!"})
            else:
                await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
                return
        else:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return

        while True:
            await websocket.receive_text()

    except WebSocketDisconnect:
        if user_id: manager.disconnect(user_id)
    except Exception:
        if user_id: manager.disconnect(user_id)
        try:
            await websocket.close(code=status.WS_1011_INTERNAL_ERROR)
        except RuntimeError:
            pass
