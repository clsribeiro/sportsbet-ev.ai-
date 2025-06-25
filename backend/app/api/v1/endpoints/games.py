from typing import List
from fastapi import APIRouter, Depends, HTTPException, status # Adicionado HTTPException e status
from sqlalchemy.ext.asyncio import AsyncSession

# Importa os schemas, CRUDs, e dependências necessários
from app.schemas.game import GameRead
from app.schemas.prediction import PredictionRead # Importa o schema de previsão
from app.crud import crud_game, crud_prediction # Importa o CRUD de previsão
from app.services import ai_prediction_service # Importa o nosso serviço de IA
from app.db.session import get_db_session
from app.api.deps.current_user import get_current_user
from app.models.user import User

router = APIRouter()
# --- NOVO ENDPOINT PARA GERAR PREVISÃO ---
@router.post(
    "/{game_id}/predict",
    response_model=PredictionRead,
    summary="Gerar ou Obter uma Previsão de IA para um Jogo",
    tags=["Jogos", "Previsões"]
)
async def generate_or_get_prediction(
    *,
    game_id: int,
    db: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user) # Protege o endpoint
):
    """
    Gera uma nova previsão de IA para um jogo se ainda não existir,
    ou retorna a previsão existente.
    """
    # 1. Verifica se o jogo existe
    game = await crud_game.get_game_by_id(db=db, game_id=game_id)
    if not game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Jogo não encontrado.",
        )

    # 2. Verifica se já existe uma previsão para este jogo
    prediction = await crud_prediction.get_prediction_by_game_id(db=db, game_id=game_id)
    if prediction:
        print(f"Retornando previsão existente para o jogo ID: {game_id}")
        return prediction

    # 3. Se não existir, gera uma nova previsão (usando o nosso serviço mock)
    print(f"Gerando nova previsão para o jogo ID: {game_id}")
    prediction_in = await ai_prediction_service.generate_prediction_for_game(game=game)

    # 4. Guarda a nova previsão no banco de dados
    new_prediction = await crud_prediction.create_prediction(db=db, prediction_in=prediction_in)

    return new_prediction
# --- FIM DO NOVO ENDPOINT ---



# --- NOVO ENDPOINT ---
@router.get(
    "/{game_id}", # Usa um parâmetro de caminho para o ID do jogo
    response_model=GameRead,
    summary="Obter Detalhes de um Jogo Específico",
    tags=["Jogos"]
)
async def get_game_details(
    *,
    game_id: int,
    db: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user) # Protege o endpoint
):
    """
    Obtém todos os detalhes de um jogo específico pelo seu ID.
    Apenas utilizadores autenticados podem aceder a este recurso.
    """
    game = await crud_game.get_game_by_id(db=db, game_id=game_id)
    if not game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Jogo não encontrado.",
        )
    return game
# --- FIM DO NOVO ENDPOINT ---


@router.get(
    "/",
    response_model=List[GameRead],
    summary="Listar Jogos Agendados",
    tags=["Jogos"]
)
async def list_games(
    db: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user) # Protege o endpoint
):
    """
    Obtém uma lista dos próximos jogos.
    Apenas utilizadores autenticados podem aceder a este recurso.
    """
    games = await crud_game.get_games(db=db, limit=20)
    return games
