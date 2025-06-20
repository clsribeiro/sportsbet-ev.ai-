import asyncio
from datetime import datetime, timedelta, timezone

# Importa a nossa sessão de banco de dados assíncrona
from app.db.session import AsyncSessionLocal

# Importa as nossas funções CRUD e os nossos schemas Pydantic
from app.crud import crud_team, crud_game
from app.schemas import TeamCreate, GameCreate, GameUpdate # Garanta que GameUpdate está importado

async def seed_data():
    """
    Popula a base de dados com equipas e jogos de exemplo, e depois atualiza
    um dos jogos com uma análise e uma dica de aposta.
    """
    print("A iniciar o processo de seeding...")
    # Cria uma nova sessão com o banco de dados
    db = AsyncSessionLocal()

    try:
        # --- Criar Equipas ---
        # A nossa função `create_team` já verifica se a equipa existe,
        # então é seguro executar esta parte múltiplas vezes.
        print("A criar/verificar equipas...")

        # Equipas de Futebol
        flamengo = await crud_team.create_team(db, team_in=TeamCreate(name="Flamengo", sport="futebol", league="Brasileirão Série A"))
        palmeiras = await crud_team.create_team(db, team_in=TeamCreate(name="Palmeiras", sport="futebol", league="Brasileirão Série A"))
        corinthians = await crud_team.create_team(db, team_in=TeamCreate(name="Corinthians", sport="futebol", league="Brasileirão Série A"))
        sao_paulo = await crud_team.create_team(db, team_in=TeamCreate(name="São Paulo", sport="futebol", league="Brasileirão Série A"))

        # Equipas da NBA
        lakers = await crud_team.create_team(db, team_in=TeamCreate(name="Los Angeles Lakers", sport="nba", league="NBA"))
        warriors = await crud_team.create_team(db, team_in=TeamCreate(name="Golden State Warriors", sport="nba", league="NBA"))

        # --- Criar Jogos de Exemplo ---
        # Nota: para um script de seed simples, assumimos que os jogos não existem.
        # Numa aplicação real, adicionaríamos uma verificação.
        print("A criar jogos de exemplo (se necessário)...")

        # Verifica se o primeiro jogo já existe para não criar duplicatas
        first_game = await crud_game.get_game_by_id(db, game_id=1)
        if not first_game:
            now = datetime.now(timezone.utc)

            game1_in = GameCreate(home_team_id=flamengo.id, away_team_id=palmeiras.id, game_time=now + timedelta(hours=2))
            game2_in = GameCreate(home_team_id=corinthians.id, away_team_id=sao_paulo.id, game_time=now + timedelta(days=1, hours=4))
            game3_in = GameCreate(home_team_id=lakers.id, away_team_id=warriors.id, game_time=now + timedelta(days=2, hours=1))

            await crud_game.create_game(db, game_in=game1_in)
            await crud_game.create_game(db, game_in=game2_in)
            await crud_game.create_game(db, game_in=game3_in)
            print("Novos jogos criados.")
        else:
            print("Jogos de exemplo já existem, a saltar a criação.")


        # --- Adicionar Análise e Dica ao Primeiro Jogo ---
        print("A adicionar/atualizar análise do primeiro jogo...")
        # Busca o jogo novamente para garantir que temos o objeto na sessão atual
        game_to_update = await crud_game.get_game_by_id(db, game_id=1)
        if game_to_update:
            analysis_update_data = GameUpdate(
                analysis="Este é um clássico de grande rivalidade. O Flamengo vem de uma sequência ofensiva forte, enquanto o Palmeiras tem a melhor defesa do campeonato. Espera-se um jogo equilibrado com poucos golos.",
                value_bet_tip="Menos de 2.5 golos (Under 2.5) parece ser a aposta de maior valor, considerando o histórico defensivo do Palmeiras e o equilíbrio do confronto."
            )
            await crud_game.update_game(db, db_game=game_to_update, game_in=analysis_update_data)
            print("Análise do jogo 1 atualizada.")

        print("Seeding concluído com sucesso!")

    finally:
        # Garante que a sessão do banco de dados seja sempre fechada
        await db.close()

# Bloco para permitir que o script seja executado diretamente
if __name__ == "__main__":
    asyncio.run(seed_data())
