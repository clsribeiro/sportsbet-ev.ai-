import asyncio

from app.db.session import AsyncSessionLocal
from app.services import football_api_service
from app.models import Team
from sqlalchemy.dialects.postgresql import insert

# --- CONFIGURAÇÃO ---
TARGET_LEAGUE_ID = 71 
TARGET_SEASON = 2023

async def sync_teams_data():
    print(f"A iniciar a sincronização de equipas para a Liga ID: {TARGET_LEAGUE_ID}, Temporada: {TARGET_SEASON}")
    db = AsyncSessionLocal()

    teams_from_api = await football_api_service.get_teams(league_id=TARGET_LEAGUE_ID, season=TARGET_SEASON)

    if not teams_from_api:
        print("Não foi possível obter equipas da API. A terminar.")
        await db.close()
        return

    teams_to_db = []
    for item in teams_from_api:
        team_data = item.get("team")
        if team_data:
            teams_to_db.append({
                "id": team_data.get("id"),
                "name": team_data.get("name"),
                "logo_url": team_data.get("logo"), # <-- CORREÇÃO AQUI
                "sport": "futebol", 
                "league": f"Brasileirão Série A - {TARGET_SEASON}"
            })

    if not teams_to_db:
        print("Nenhuma equipa encontrada na resposta da API.")
        await db.close()
        return

    print(f"Encontradas {len(teams_to_db)} equipas na API. A inserir/atualizar na base de dados...")

    try:
        stmt = insert(Team).values(teams_to_db)

        update_dict = {
            'name': stmt.excluded.name,
            'logo_url': stmt.excluded.logo_url, # <-- CORREÇÃO AQUI
            'league': stmt.excluded.league,
        }
        stmt = stmt.on_conflict_do_update(
            index_elements=['id'],
            set_=update_dict
        )

        await db.execute(stmt)
        await db.commit()
        print("Sincronização de equipas concluída.")
    finally:
        await db.close()

if __name__ == "__main__":
    asyncio.run(sync_teams_data())
