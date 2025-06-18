from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.team import Team
from app.schemas.team import TeamCreate

async def create_team(db: AsyncSession, *, team_in: TeamCreate) -> Team:
    """Cria uma nova equipa se ela não existir."""
    # Verifica se a equipa já existe pelo nome
    result = await db.execute(select(Team).filter(Team.name == team_in.name))
    existing_team = result.scalars().first()
    if existing_team:
        return existing_team

    db_team = Team(**team_in.model_dump())
    db.add(db_team)
    await db.commit()
    await db.refresh(db_team)
    return db_team
