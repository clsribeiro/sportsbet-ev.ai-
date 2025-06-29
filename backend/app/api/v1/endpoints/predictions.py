from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.prediction import PredictionReadWithGame 
from app.crud import crud_prediction
from app.db.session import get_db_session
# MUDANÇA: Importamos a nossa nova dependência 'require_permission'
from app.api.deps.current_user import require_permission 
from app.models.user import User

router = APIRouter()

@router.get(
    "/",
    response_model=List[PredictionReadWithGame],
    summary="Listar Dicas e Previsões da IA",
    tags=["Previsões"]
)
async def list_predictions(
    db: AsyncSession = Depends(get_db_session),
    # MUDANÇA: Em vez de apenas verificar se o utilizador está autenticado,
    # agora exigimos que ele tenha uma permissão específica.
    current_user: User = Depends(require_permission("feature:access_advanced_analysis"))
):
    """
    Obtém uma lista das previsões mais recentes geradas pela IA.
    
    Este é um recurso protegido e requer que o utilizador tenha a permissão 
    'feature:access_advanced_analysis' através de um dos seus planos.
    """
    predictions = await crud_prediction.get_predictions(db=db, limit=20)
    return predictions

