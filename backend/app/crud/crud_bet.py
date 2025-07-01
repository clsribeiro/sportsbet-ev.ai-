from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from typing import List
from uuid import UUID

from app.models.bet import Bet
from app.schemas.bet import BetCreate

async def create_bet(db: AsyncSession, *, bet_in: BetCreate, user_id: UUID) -> Bet:
    """
    Cria uma nova aposta para um utilizador específico.
    """
    # Cria uma instância do modelo Bet com os dados do schema e o user_id
    db_bet = Bet(**bet_in.model_dump(), user_id=user_id)
    db.add(db_bet)
    await db.commit()
    await db.refresh(db_bet)
    return db_bet

async def get_bets_by_user(
    db: AsyncSession, *, user_id: UUID, skip: int = 0, limit: int = 100
) -> List[Bet]:
    """
    Busca uma lista de todas as apostas de um utilizador específico.
    """
    result = await db.execute(
        select(Bet)
        .where(Bet.user_id == user_id)
        .order_by(Bet.placed_at.desc()) # Ordena pelas mais recentes
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()
