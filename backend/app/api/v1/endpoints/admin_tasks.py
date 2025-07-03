from fastapi import APIRouter, Depends, Body, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.services import pre_analysis_service
from app.db.session import get_db_session
from app.api.deps.current_user import get_current_superuser
from app.models.user import User
from app.websocket_manager import manager

router = APIRouter()

@router.post(
    "/run-pre-analysis",
    summary="Acionar o Serviço de Pré-Análise de Jogos",
    tags=["Admin - Tarefas"]
)
async def trigger_pre_analysis(
    db: AsyncSession = Depends(get_db_session),
    current_superuser: User = Depends(get_current_superuser),
):
    """Aciona manualmente o serviço de fundo para gerar previsões de IA."""
    result = await pre_analysis_service.run_pre_analysis_for_upcoming_games(db=db, limit=5)
    return result

@router.post(
    "/broadcast-test",
    summary="Enviar Mensagem de Teste via WebSocket",
    status_code=status.HTTP_202_ACCEPTED,
    tags=["Admin - Tarefas"]
)
async def broadcast_test_message(
    message: str = Body(..., embed=True, description="A mensagem a ser enviada."),
    current_superuser: User = Depends(get_current_superuser),
):
    """Envia uma mensagem de teste para todos os clientes WebSocket conectados."""
    print(f"Admin '{current_superuser.email}' a enviar broadcast: '{message}'")
    await manager.broadcast(message)
    return {"detail": "Mensagem de broadcast enviada para todos os clientes conectados."}
