import asyncio
from datetime import datetime, timedelta, timezone

from app.db.session import AsyncSessionLocal
from app.crud import crud_team, crud_game
from app.schemas import TeamCreate, GameCreate

async def seed_data():
    print("A iniciar o processo de seeding...")
    db = AsyncSessionLocal()
    try:
        # --- Criar Equipas de Futebol (Brasileirão) ---
        print("A criar equipas de futebol...")
        flamengo_in = TeamCreate(name="Flamengo", sport="futebol", league="Brasileirão Série A")
        palmeiras_in = TeamCreate(name="Palmeiras", sport="futebol", league="Brasileirão Série A")
        corinthians_in = TeamCreate(name="Corinthians", sport="futebol", league="Brasileirão Série A")
        sao_paulo_in = TeamCreate(name="São Paulo", sport="futebol", league="Brasileirão Série A")

        flamengo = await crud_team.create_team(db, team_in=flamengo_in)
        palmeiras = await crud_team.create_team(db, team_in=palmeiras_in)
        corinthians = await crud_team.create_team(db, team_in=corinthians_in)
        sao_paulo = await crud_team.create_team(db, team_in=sao_paulo_in)

        # --- Criar Equipas da NBA ---
        print("A criar equipas da NBA...")
        lakers_in = TeamCreate(name="Los Angeles Lakers", sport="nba", league="NBA")
        warriors_in = TeamCreate(name="Golden State Warriors", sport="nba", league="NBA")

        lakers = await crud_team.create_team(db, team_in=lakers_in)
        warriors = await crud_team.create_team(db, team_in=warriors_in)

        # --- Criar Jogos de Exemplo ---
        print("A criar jogos de exemplo...")
        now = datetime.now(timezone.utc)

        game1_in = GameCreate(
            home_team_id=flamengo.id,
            away_team_id=palmeiras.id,
            game_time=now + timedelta(hours=2)
        )
        game2_in = GameCreate(
            home_team_id=corinthians.id,
            away_team_id=sao_paulo.id,
            game_time=now + timedelta(days=1, hours=4)
        )
        game3_in = GameCreate(
            home_team_id=lakers.id,
            away_team_id=warriors.id,
            game_time=now + timedelta(days=2, hours=1)
        )

        await crud_game.create_game(db, game_in=game1_in)
        await crud_game.create_game(db, game_in=game2_in)
        await crud_game.create_game(db, game_in=game3_in)

        print("Seeding concluído com sucesso!")

    finally:
        await db.close()

if __name__ == "__main__":
    asyncio.run(seed_data())
