from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

# Usaremos o novo schema que inclui os dados do jogo
from app.schemas.prediction import PredictionReadWithGame 
from app.crud import crud_prediction
from app.db.session import get_db_session
from app.api.deps.current_user import get_current_user
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
    current_user: User = Depends(get_current_user) # Protege o endpoint
):
    """
    Obtém uma lista das previsões mais recentes geradas pela IA.
    Apenas utilizadores autenticados podem aceder.
    """
    predictions = await crud_prediction.get_predictions(db=db, limit=20)
    return predictions
