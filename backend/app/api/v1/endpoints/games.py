from typing import List
from fastapi import APIRouter, Depends, HTTPException, status # Adicionado HTTPException e status
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.game import GameRead
from app.crud import crud_game
from app.db.session import get_db_session
from app.api.deps.current_user import get_current_user
from app.models.user import User

router = APIRouter()

# --- NOVO ENDPOINT ---
@router.get(
    "/{game_id}", # Usa um parâmetro de caminho para o ID do jogo
    response_model=GameRead,
    summary="Obter Detalhes de um Jogo Específico",
    tags=["Jogos"]
)
async def get_game_details(
    *,
    game_id: int,
    db: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user) # Protege o endpoint
):
    """
    Obtém todos os detalhes de um jogo específico pelo seu ID.
    Apenas utilizadores autenticados podem aceder a este recurso.
    """
    game = await crud_game.get_game_by_id(db=db, game_id=game_id)
    if not game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Jogo não encontrado.",
        )
    return game
# --- FIM DO NOVO ENDPOINT ---


@router.get(
    "/",
    response_model=List[GameRead],
    summary="Listar Jogos Agendados",
    tags=["Jogos"]
)
async def list_games(
    db: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user) # Protege o endpoint
):
    """
    Obtém uma lista dos próximos jogos.
    Apenas utilizadores autenticados podem aceder a este recurso.
    """
    games = await crud_game.get_games(db=db, limit=20)
    return games
