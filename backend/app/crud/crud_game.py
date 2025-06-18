from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload # Importante para carregamento eficiente

from app.models.game import Game
from app.schemas.game import GameCreate

async def get_games(db: AsyncSession, *, skip: int = 0, limit: int = 100) -> list[Game]:
    """Busca uma lista de jogos, carregando os dados das equipas relacionadas."""
    result = await db.execute(
        select(Game)
        .options(selectinload(Game.home_team), selectinload(Game.away_team)) # Carrega as equipas
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
