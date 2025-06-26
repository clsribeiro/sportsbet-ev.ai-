import google.generativeai as genai
import json
import re
from typing import Dict, Any

from app.core.config import settings
from app.models.game import Game
from app.schemas.prediction import PredictionCreate

# Configura a API do Google AI com a sua chave
try:
    genai.configure(api_key=settings.GOOGLE_API_KEY)
    # Configurações de segurança para o modelo
    safety_settings = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
    ]
    # Seleciona o modelo a ser usado. 'gemini-1.5-flash' é rápido e eficiente.
    model = genai.GenerativeModel('gemini-1.5-flash', safety_settings=safety_settings)
    print("Modelo Gemini configurado com sucesso.")
except Exception as e:
    print(f"ERRO ao configurar o modelo Gemini: {e}")
    model = None


def parse_ai_response(text_response: str, game: Game) -> Dict[str, Any]:
    """
    Analisa a resposta de texto da IA para extrair dados estruturados.
    """
    # Remove ```json e ``` do início e fim, se existirem
    if text_response.strip().startswith("```json"):
        text_response = text_response.strip()[7:-3].strip()

    try:
        data = json.loads(text_response)
        return {
            "predicted_winner": data.get("vencedor_previsto"),
            "prediction_summary": data.get("resumo_analise"),
            "value_bet_suggestion": data.get("sugestao_aposta_valor"),
            "home_win_probability": data.get("probabilidade_vitoria_casa"),
            "away_win_probability": data.get("probabilidade_vitoria_fora"),
            "draw_probability": data.get("probabilidade_empate"),
            "confidence_level": data.get("nivel_confianca"),
        }
    except (json.JSONDecodeError, KeyError) as e:
        print(f"Erro ao analisar o JSON da resposta da IA: {e}")
        # Fallback se o JSON falhar: tenta usar a resposta de texto diretamente
        return {
            "predicted_winner": game.home_team.name if game.home_team.name in text_response else game.away_team.name,
            "prediction_summary": text_response,
            "value_bet_suggestion": "Não foi possível extrair a dica de aposta.",
            "confidence_level": 0.5, # Nível de confiança padrão
        }


async def generate_prediction_for_game(game: Game) -> PredictionCreate:
    """
    Gera uma previsão para um jogo específico usando o modelo Gemini.
    """
    print(f"A gerar predição com IA para o jogo ID: {game.id}...")

    if not model:
        raise Exception("O modelo Gemini não está configurado. Verifique a chave de API.")

    # 1. Construir o Prompt
    # Este é o "cérebro" da nossa pergunta. Um prompt bem elaborado resulta numa resposta melhor.
    prompt = f"""
    **Análise de Jogo de Futebol para Apostas de Valor**

    **Contexto:** Você é um analista desportivo especialista, focado em encontrar apostas de valor (EV+).
    Sua tarefa é analisar o seguinte jogo e fornecer uma previsão estruturada.

    **Dados do Jogo:**
    - **Liga:** {game.home_team.league}
    - **Equipa da Casa:** {game.home_team.name}
    - **Equipa de Fora:** {game.away_team.name}
    - **Data do Jogo:** {game.game_time.strftime('%d/%m/%Y')}

    **Instruções de Resposta:**
    Responda **exclusivamente** com um objeto JSON válido, sem nenhum texto adicional antes ou depois.
    O JSON deve ter a seguinte estrutura e tipos de dados:
    {{
      "vencedor_previsto": "string",
      "probabilidade_vitoria_casa": "float (ex: 0.45)",
      "probabilidade_vitoria_fora": "float (ex: 0.30)",
      "probabilidade_empate": "float (ex: 0.25)",
      "nivel_confianca": "float (0.0 a 1.0, representando a confiança geral na análise)",
      "resumo_analise": "string (Um parágrafo conciso com a sua análise tática, considerando a forma atual, confrontos diretos e fatores chave)",
      "sugestao_aposta_valor": "string (A sua principal recomendação de aposta de valor, explicando o porquê, ex: 'Handicap Asiático -0.5 para a Equipa da Casa' ou 'Mais de 2.5 golos')"
    }}

    **Análise Requerida:**
    Com base nos nomes das equipas e na liga, realize a sua análise. Lembre-se, o objetivo é encontrar valor.
    """

    try:
        # 2. Enviar o Prompt para a API do Gemini
        print("A enviar pedido para a API do Gemini...")
        response = await model.generate_content_async(prompt)

        # 3. Processar a Resposta
        print("Resposta da IA recebida. A analisar...")
        ai_text_response = response.text
        parsed_data = parse_ai_response(ai_text_response, game)

        # 4. Criar o objeto de previsão
        prediction_data = PredictionCreate(
            game_id=game.id,
            model_version="gemini-1.5-flash-v1",
            **parsed_data
        )
        return prediction_data

    except Exception as e:
        print(f"ERRO ao gerar conteúdo com o Gemini: {e}")
        # Em caso de falha da API, podemos retornar uma previsão de erro ou levantar uma exceção
        raise Exception("Falha ao comunicar com o serviço de IA.")
