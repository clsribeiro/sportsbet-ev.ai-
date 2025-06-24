import asyncio
from datetime import datetime

from app.db.session import AsyncSessionLocal
from app.services import football_api_service
from app.models import Game, GameStatus
from sqlalchemy.dialects.postgresql import insert

# --- CONFIGURAÇÃO ---
# Usaremos a mesma liga e temporada que usámos para as equipas
TARGET_LEAGUE_ID = 71 
TARGET_SEASON = 2023

# Mapeamento do status da API para o nosso Enum de status
STATUS_MAP = {
    "TBD": GameStatus.SCHEDULED,
    "NS": GameStatus.SCHEDULED,
    "1H": GameStatus.IN_PROGRESS,
    "HT": GameStatus.IN_PROGRESS,
    "2H": GameStatus.IN_PROGRESS,
    "ET": GameStatus.IN_PROGRESS,
    "BT": GameStatus.IN_PROGRESS,
    "P": GameStatus.IN_PROGRESS,
    "SUSP": GameStatus.POSTPONED,
    "INT": GameStatus.POSTPONED,
    "FT": GameStatus.FINISHED,
    "AET": GameStatus.FINISHED,
    "PEN": GameStatus.FINISHED,
    "PST": GameStatus.POSTPONED,
    "CANC": GameStatus.CANCELLED,
    "ABD": GameStatus.CANCELLED,
    "AWD": GameStatus.FINISHED,
    "WO": GameStatus.FINISHED,
}

async def sync_games_data():
    print(f"A iniciar a sincronização de jogos para a Liga ID: {TARGET_LEAGUE_ID}, Temporada: {TARGET_SEASON}")
    db = AsyncSessionLocal()

    fixtures_from_api = await football_api_service.get_fixtures(league_id=TARGET_LEAGUE_ID, season=TARGET_SEASON)

    if not fixtures_from_api:
        print("Não foi possível obter jogos da API. A terminar.")
        await db.close()
        return

    games_to_db = []
    for item in fixtures_from_api:
        fixture_data = item.get("fixture", {})
        teams_data = item.get("teams", {})
        goals_data = item.get("goals", {})

        # Garante que temos todos os dados essenciais antes de prosseguir
        if fixture_data.get("id") and teams_data.get("home", {}).get("id") and teams_data.get("away", {}).get("id"):
            game_status_short = fixture_data.get("status", {}).get("short", "TBD")

            games_to_db.append({
                "id": fixture_data.get("id"),
                "home_team_id": teams_data.get("home").get("id"),
                "away_team_id": teams_data.get("away").get("id"),
                "game_time": datetime.fromisoformat(fixture_data.get("date")),
                "status": STATUS_MAP.get(game_status_short, GameStatus.SCHEDULED),
                "home_score": goals_data.get("home"),
                "away_score": goals_data.get("away"),
                "api_provider": "api-football",
                "api_game_id": str(fixture_data.get("id"))
            })

    if not games_to_db:
        print("Nenhum jogo formatado a partir da resposta da API.")
        await db.close()
        return

    print(f"Encontrados {len(games_to_db)} jogos na API. A inserir/atualizar na base de dados...")

    try:
        stmt = insert(Game).values(games_to_db)
        update_dict = {
            'game_time': stmt.excluded.game_time,
            'status': stmt.excluded.status,
            'home_score': stmt.excluded.home_score,
            'away_score': stmt.excluded.away_score,
        }
        stmt = stmt.on_conflict_do_update(
            index_elements=['id'],
            set_=update_dict
        )

        await db.execute(stmt)
        await db.commit()
        print("Sincronização de jogos concluída.")
    finally:
        await db.close()

if __name__ == "__main__":
    asyncio.run(sync_games_data())
