from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.bet import BetRead, BetCreate
from app.crud import crud_bet
from app.db.session import get_db_session
from app.api.deps.current_user import get_current_user
from app.models.user import User

router = APIRouter()

@router.post(
    "/",
    response_model=BetRead,
    status_code=status.HTTP_201_CREATED,
    summary="Registar uma Nova Aposta",
    tags=["Apostas (Bet Tracker)"]
)
async def create_new_bet(
    *,
    bet_in: BetCreate,
    db: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user)
):
    """
    Regista uma nova aposta para o utilizador atualmente autenticado.
    """
    bet = await crud_bet.create_bet(db=db, bet_in=bet_in, user_id=current_user.id)
    return bet

@router.get(
    "/",
    response_model=List[BetRead],
    summary="Listar as Apostas do Utilizador",
    tags=["Apostas (Bet Tracker)"]
)
async def list_user_bets(
    db: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user)
):
    """
    Obtém uma lista de todas as apostas registadas pelo utilizador autenticado.
    """
    bets = await crud_bet.get_bets_by_user(db=db, user_id=current_user.id)
    return bets
