from sqlalchemy.ext.asyncio import AsyncSession
from app.crud import crud_game, crud_prediction
from app.services import ai_prediction_service
import asyncio

async def run_pre_analysis_for_upcoming_games(db: AsyncSession, limit: int = 5):
    """
    Busca jogos futuros sem previsão e aciona a geração de análise de IA para eles.

    Numa aplicação real, isto seria executado por uma tarefa agendada (cron job).
    Para o nosso propósito, será acionado por um endpoint de admin.
    """
    print("A iniciar o serviço de pré-análise...")

    # 1. Encontrar jogos que precisam de análise
    games_to_analyze = await crud_game.get_upcoming_games_without_prediction(db=db, limit=limit)

    if not games_to_analyze:
        print("Nenhum jogo novo para analisar.")
        return {"message": "Nenhum jogo novo para analisar.", "analyzed_count": 0}

    print(f"Encontrados {len(games_to_analyze)} jogos para analisar. A gerar previsões...")

    # 2. Gerar e guardar a previsão para cada jogo
    tasks = []
    for game in games_to_analyze:
        # Cria uma "tarefa" para gerar a previsão para cada jogo.
        # Isto permite que, no futuro, possamos executá-las em paralelo se quisermos.
        prediction_in = await ai_prediction_service.generate_prediction_for_game(game=game)
        tasks.append(crud_prediction.create_prediction(db=db, prediction_in=prediction_in))

    # Executa todas as tarefas de criação de previsão
    await asyncio.gather(*tasks)

    print(f"Pré-análise concluída para {len(games_to_analyze)} jogos.")
    return {
        "message": f"Pré-análise concluída para {len(games_to_analyze)} jogos.",
        "analyzed_count": len(games_to_analyze)
    }
