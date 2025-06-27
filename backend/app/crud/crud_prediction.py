from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from typing import List

from app.models.prediction import Prediction
from app.models.game import Game # Importar Game para o relacionamento
from app.schemas.prediction import PredictionCreate

async def get_prediction_by_game_id(db: AsyncSession, *, game_id: int) -> Prediction | None:
    """Busca uma previsão pelo ID do jogo."""
    result = await db.execute(
        select(Prediction).filter(Prediction.game_id == game_id)
    )
    return result.scalars().first()

# --- NOVA FUNÇÃO ---
async def get_predictions(db: AsyncSession, *, skip: int = 0, limit: int = 20) -> List[Prediction]:
    """Busca as previsões mais recentes, carregando os dados dos jogos e equipas."""
    result = await db.execute(
        select(Prediction)
        .join(Prediction.game) # Faz o JOIN com a tabela de jogos
        # Carrega de forma otimizada o jogo e as equipas relacionadas
        .options(
            selectinload(Prediction.game)
            .selectinload(Game.home_team)
        )
        .options(
            selectinload(Prediction.game)
            .selectinload(Game.away_team)
        )
        .order_by(Prediction.created_at.desc()) # Ordena pelas mais recentes
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()


async def create_prediction(db: AsyncSession, *, prediction_in: PredictionCreate) -> Prediction:
    """Cria uma nova previsão na base de dados."""
    db_prediction = Prediction(**prediction_in.model_dump())
    db.add(db_prediction)
    await db.commit()
    await db.refresh(db_prediction)
    return db_prediction