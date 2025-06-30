from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from datetime import datetime, timezone, timedelta
from typing import List

from app.models.game import Game, GameStatus
from app.models.prediction import Prediction
from app.schemas.game import GameCreate, GameUpdate

async def get_game_by_id(db: AsyncSession, *, game_id: int) -> Game | None:
    """Busca um único jogo pelo seu ID, carregando os dados das equipas."""
    result = await db.execute(
        select(Game)
        .where(Game.id == game_id)
        .options(selectinload(Game.home_team), selectinload(Game.away_team))
    )
    return result.scalars().first()

# --- FUNÇÃO MODIFICADA ---
async def get_games(
    db: AsyncSession, *, 
    time_filter: str = "upcoming", 
    skip: int = 0, 
    limit: int = 100
) -> list[Game]:
    """
    Busca uma lista de jogos, com um filtro de tempo opcional.
    Filtros: 'live', 'today', 'upcoming'.
    """
    now = datetime.now(timezone.utc)
    
    query = select(Game).options(
        selectinload(Game.home_team), selectinload(Game.away_team)
    )

    if time_filter == "live":
        query = query.where(Game.status == GameStatus.IN_PROGRESS).order_by(Game.game_time.asc())
    elif time_filter == "today":
        start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = start_of_day + timedelta(days=1)
        query = query.where(
            Game.game_time >= start_of_day,
            Game.game_time < end_of_day,
            Game.status == GameStatus.SCHEDULED
        ).order_by(Game.game_time.asc())
    else: # "upcoming" é o padrão
        start_of_tomorrow = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_week = start_of_tomorrow + timedelta(days=7)
        query = query.where(
            Game.game_time >= start_of_tomorrow,
            Game.game_time < end_of_week,
            Game.status == GameStatus.SCHEDULED
        ).order_by(Game.game_time.asc())
        
    query = query.offset(skip).limit(limit)
    
    result = await db.execute(query)
    return result.scalars().all()


async def create_game(db: AsyncSession, *, game_in: GameCreate) -> Game:
    """Cria um novo jogo."""
    db_game = Game(**game_in.model_dump())
    db.add(db_game)
    await db.commit()
    await db.refresh(db_game)
    return db_game


async def update_game(db: AsyncSession, *, db_game: Game, game_in: GameUpdate) -> Game:
    """Atualiza os dados de um jogo."""
    update_data = game_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_game, field, value)
    
    db.add(db_game)
    await db.commit()
    await db.refresh(db_game)
    return db_game


async def get_upcoming_games_without_prediction(db: AsyncSession, limit: int = 5) -> List[Game]:
    """
    Busca os próximos jogos agendados que ainda não têm uma previsão associada.
    """
    now = datetime.now(timezone.utc)
    subquery = select(Prediction.game_id)
    
    result = await db.execute(
        select(Game)
        .outerjoin(Prediction)
        .where(
            Game.game_time > now,
            Game.status == GameStatus.SCHEDULED,
            Game.id.not_in(subquery)
        )
        .options(selectinload(Game.home_team), selectinload(Game.away_team))
        .order_by(Game.game_time.asc())
        .limit(limit)
    )
    return result.scalars().all()
