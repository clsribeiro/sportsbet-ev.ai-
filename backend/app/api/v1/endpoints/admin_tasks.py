from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.services import pre_analysis_service
from app.db.session import get_db_session
from app.api.deps.current_user import get_current_superuser
from app.models.user import User

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
    """
    Aciona manualmente o serviço de fundo para buscar jogos futuros
    e gerar previsões de IA para eles.

    Apenas superutilizadores podem aceder.
    """
    result = await pre_analysis_service.run_pre_analysis_for_upcoming_games(db=db, limit=5)
    return result
