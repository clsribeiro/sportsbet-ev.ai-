from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.prediction import Prediction
from app.schemas.prediction import PredictionCreate

async def get_prediction_by_game_id(db: AsyncSession, *, game_id: int) -> Prediction | None:
    """Busca uma previsão pelo ID do jogo."""
    result = await db.execute(
        select(Prediction).filter(Prediction.game_id == game_id)
    )
    return result.scalars().first()

async def create_prediction(db: AsyncSession, *, prediction_in: PredictionCreate) -> Prediction:
    """Cria uma nova previsão no banco de dados."""
    db_prediction = Prediction(**prediction_in.model_dump())
    db.add(db_prediction)
    await db.commit()
    await db.refresh(db_prediction)
    return db_prediction
