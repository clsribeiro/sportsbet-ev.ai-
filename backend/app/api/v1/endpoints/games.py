from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.game import GameRead
from app.schemas.prediction import PredictionRead
from app.crud import crud_game, crud_prediction
from app.services import ai_prediction_service
from app.db.session import get_db_session
from app.api.deps.current_user import get_current_user
from app.models.user import User

router = APIRouter()

@router.get(
    "/{game_id}",
    response_model=GameRead,
    summary="Obter Detalhes de um Jogo Específico",
    tags=["Jogos"]
)
async def get_game_details(
    *,
    game_id: int,
    db: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user)
):
    """Obtém todos os detalhes de um jogo específico pelo seu ID."""
    game = await crud_game.get_game_by_id(db=db, game_id=game_id)
    if not game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Jogo não encontrado.",
        )
    return game

# --- ENDPOINT MODIFICADO ---
@router.get(
    "/",
    response_model=List[GameRead],
    summary="Listar Jogos Agendados",
    tags=["Jogos"]
)
async def list_games(
    *,
    db: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
    # Adicionamos um parâmetro de query para o filtro de tempo
    time_filter: Optional[str] = Query("upcoming", enum=["live", "today", "upcoming"])
):
    """
    Obtém uma lista de jogos, que pode ser filtrada por tempo.
    - **live**: Jogos atualmente em progresso.
    - **today**: Jogos agendados para hoje.
    - **upcoming**: Jogos agendados para os próximos 7 dias (padrão).
    """
    games = await crud_game.get_games(db=db, limit=100, time_filter=time_filter)
    return games

@router.post(
    "/{game_id}/predict",
    response_model=PredictionRead,
    summary="Gerar ou Obter uma Previsão de IA para um Jogo",
    tags=["Jogos", "Previsões"]
)
async def generate_or_get_prediction(
    *,
    game_id: int,
    db: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user)
):
    """Gera uma nova previsão de IA para um jogo se ainda não existir, ou retorna a existente."""
    game = await crud_game.get_game_by_id(db=db, game_id=game_id)
    if not game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Jogo não encontrado.",
        )
    
    prediction = await crud_prediction.get_prediction_by_game_id(db=db, game_id=game_id)
    if prediction:
        return prediction

    prediction_in = await ai_prediction_service.generate_prediction_for_game(game=game)
    new_prediction = await crud_prediction.create_prediction(db=db, prediction_in=prediction_in)
    
    return new_prediction
