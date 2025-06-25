from app.models.game import Game
from app.schemas.prediction import PredictionCreate
import random

async def generate_prediction_for_game(game: Game) -> PredictionCreate:
    """
    Gera uma previsão para um jogo específico.

    NOTA: Esta é uma implementação MOCK (de exemplo). No futuro, esta função
    irá formatar um prompt com os dados do jogo e chamar uma API de IA (ex: Gemini).
    """
    print(f"A gerar predição MOCK para o jogo ID: {game.id}...")

    # Lógica de exemplo super simples
    teams = [game.home_team.name, game.away_team.name]
    winner = random.choice(teams)
    confidence = round(random.uniform(0.55, 0.85), 2)

    summary = (
        f"Análise preliminar para {game.home_team.name} vs {game.away_team.name}. "
        f"Considerando a forma recente e os confrontos diretos, o nosso modelo "
        f"atribui uma ligeira vantagem ao {winner}."
    )
    tip = (
        f"A aposta de valor identificada é 'Moneyline - {winner}' "
        f"com uma confiança de {confidence * 100:.0f}%. Comparar com odds acima de {1/confidence:.2f}."
    )

    prediction_data = PredictionCreate(
        game_id=game.id,
        predicted_winner=winner,
        prediction_summary=summary,
        value_bet_suggestion=tip,
        home_win_probability=confidence if winner == game.home_team.name else 1 - confidence,
        away_win_probability=confidence if winner == game.away_team.name else 1 - confidence,
        draw_probability=0.05, # Placeholder
        confidence_level=confidence,
        model_version="mock_v0.1"
    )

    return prediction_data
