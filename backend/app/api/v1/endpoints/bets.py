from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.bet import BetRead, BetCreate, BetUpdate
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
    """Regista uma nova aposta para o utilizador atualmente autenticado."""
    return await crud_bet.create_bet(db=db, bet_in=bet_in, user_id=current_user.id)

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
    """Obtém uma lista de todas as apostas registadas pelo utilizador autenticado."""
    return await crud_bet.get_bets_by_user(db=db, user_id=current_user.id)

@router.put(
    "/{bet_id}",
    response_model=BetRead,
    summary="Atualizar o Status de uma Aposta",
    tags=["Apostas (Bet Tracker)"]
)
async def update_bet_status(
    *,
    bet_id: int,
    bet_in: BetUpdate,
    db: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user)
):
    """Atualiza o status de uma aposta (ex: para 'won' ou 'lost')."""
    db_bet = await crud_bet.get_bet_by_id(db=db, bet_id=bet_id, user_id=current_user.id)
    if not db_bet:
        raise HTTPException(status_code=404, detail="Aposta não encontrada ou não pertence a este utilizador.")
    return await crud_bet.update_bet(db=db, db_bet=db_bet, bet_in=bet_in)

# --- NOVO ENDPOINT ---
@router.delete(
    "/{bet_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Apagar uma Aposta",
    tags=["Apostas (Bet Tracker)"]
)
async def delete_user_bet(
    *,
    bet_id: int,
    db: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user)
):
    """Apaga uma aposta específica do utilizador."""
    db_bet = await crud_bet.get_bet_by_id(db=db, bet_id=bet_id, user_id=current_user.id)
    if not db_bet:
        raise HTTPException(status_code=404, detail="Aposta não encontrada ou não pertence a este utilizador.")
    
    await crud_bet.delete_bet(db=db, db_bet=db_bet)
    return

