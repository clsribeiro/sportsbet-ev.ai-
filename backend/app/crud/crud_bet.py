from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from uuid import UUID

from app.models.bet import Bet
from app.schemas.bet import BetCreate, BetUpdate

async def get_bet_by_id(db: AsyncSession, *, bet_id: int, user_id: UUID) -> Bet | None:
    """Busca uma aposta específica pelo seu ID, garantindo que pertence ao utilizador."""
    result = await db.execute(
        select(Bet).where(Bet.id == bet_id, Bet.user_id == user_id)
    )
    return result.scalars().first()

async def update_bet(db: AsyncSession, *, db_bet: Bet, bet_in: BetUpdate) -> Bet:
    """Atualiza os dados de uma aposta (principalmente o status)."""
    update_data = bet_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_bet, field, value)
    
    db.add(db_bet)
    await db.commit()
    await db.refresh(db_bet)
    return db_bet

# --- NOVA FUNÇÃO ---
async def delete_bet(db: AsyncSession, *, db_bet: Bet) -> None:
    """Apaga uma aposta do banco de dados."""
    await db.delete(db_bet)
    await db.commit()
    return

async def create_bet(db: AsyncSession, *, bet_in: BetCreate, user_id: UUID) -> Bet:
    """Cria uma nova aposta para um utilizador específico."""
    db_bet = Bet(**bet_in.model_dump(), user_id=user_id)
    db.add(db_bet)
    await db.commit()
    await db.refresh(db_bet)
    return db_bet

async def get_bets_by_user(
    db: AsyncSession, *, user_id: UUID, skip: int = 0, limit: int = 100
) -> List[Bet]:
    """Busca uma lista de todas as apostas de um utilizador específico."""
    result = await db.execute(
        select(Bet)
        .where(Bet.user_id == user_id)
        .order_by(Bet.placed_at.desc()) # Ordena pelas mais recentes
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()
