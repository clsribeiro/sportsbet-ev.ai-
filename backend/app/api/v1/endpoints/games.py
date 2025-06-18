from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.game import GameRead
from app.crud import crud_game
from app.db.session import get_db_session
from app.api.deps.current_user import get_current_user
from app.models.user import User

router = APIRouter()

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
