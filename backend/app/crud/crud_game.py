from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.models.game import Game
from app.schemas.game import GameCreate, GameUpdate # Adicionado GameUpdate

# NOVA FUNÇÃO: para buscar um jogo específico
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
        .options(selectinload(Game.home_team), selectinload(Game.away_team)) # Carrega as equipas
        .order_by(Game.game_time.asc())
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()


async def create_game(db: AsyncSession, *, game_in: GameCreate) -> Game:
    """Cria um novo jogo."""
    # model_dump() é para Pydantic v2
    db_game = Game(**game_in.model_dump())
    db.add(db_game)
    await db.commit()
    await db.refresh(db_game)
    return db_game


# NOVA FUNÇÃO: para atualizar um jogo com análise/dica
async def update_game(db: AsyncSession, *, db_game: Game, game_in: GameUpdate) -> Game:
    """Atualiza os dados de um jogo."""
    # Pega apenas os campos que foram enviados na requisição para não apagar os existentes
    update_data = game_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_game, field, value)
    
    db.add(db_game)
    await db.commit()
    await db.refresh(db_game)
    return db_game
