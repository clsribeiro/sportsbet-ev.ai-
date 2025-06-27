from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from datetime import datetime, timezone
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

async def get_games(db: AsyncSession, *, skip: int = 0, limit: int = 100) -> list[Game]:
    """Busca uma lista de jogos, carregando os dados das equipas relacionadas."""
    result = await db.execute(
        select(Game)
        .options(selectinload(Game.home_team), selectinload(Game.away_team))
        .order_by(Game.game_time.asc())
        .offset(skip)
        .limit(limit)
    )
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
