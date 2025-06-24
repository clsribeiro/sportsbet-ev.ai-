import asyncio
from app.db.session import AsyncSessionLocal
from app.services import football_api_service
# A importação do schema LeagueCreate não é estritamente necessária aqui, mas podemos deixar
from app.schemas import LeagueCreate 
from app.models import League

# --- INÍCIO DA CORREÇÃO ---
# Importar a construção 'insert' específica do dialeto do PostgreSQL
from sqlalchemy.dialects.postgresql import insert
# --- FIM DA CORREÇÃO ---

async def sync_leagues_data():
    print("A iniciar a sincronização de ligas...")
    db = AsyncSessionLocal()

    leagues_from_api = await football_api_service.get_leagues()

    if not leagues_from_api:
        print("Não foi possível obter ligas da API. A terminar.")
        await db.close()
        return

    leagues_to_db = []
    for item in leagues_from_api:
        league_data = item.get("league")
        country_data = item.get("country")
        if league_data and country_data:
            leagues_to_db.append({
                "id": league_data.get("id"),
                "name": league_data.get("name"),
                "type": league_data.get("type"),
                "logo": league_data.get("logo"),
                "country": country_data.get("name")
            })

    if not leagues_to_db:
        print("Nenhuma liga encontrada na resposta da API.")
        await db.close()
        return

    print(f"Encontradas {len(leagues_to_db)} ligas na API. A inserir/ignorar na base de dados...")

    try:
        # --- INÍCIO DA CORREÇÃO ---
        # Usa a construção 'insert' importada do dialeto do PostgreSQL
        stmt = insert(League).values(leagues_to_db)

        # Define a política de conflito para a chave primária 'id'
        # Se uma liga com o mesmo ID já existir, não faz nada (ignora).
        stmt = stmt.on_conflict_do_nothing(
            index_elements=['id']
        )
        # --- FIM DA CORREÇÃO ---

        await db.execute(stmt)
        await db.commit()
        print("Sincronização de ligas concluída.")
    finally:
        await db.close()

if __name__ == "__main__":
    asyncio.run(sync_leagues_data())
