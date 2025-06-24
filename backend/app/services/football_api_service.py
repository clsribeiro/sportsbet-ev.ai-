import httpx
from typing import Optional, Dict, Any, List # Adicionado 'List' aqui

# Importa as nossas configurações centrais
from app.core.config import settings

# URL base da API
BASE_URL = "https://v3.football.api-sports.io"

# Cabeçalhos padrão que serão enviados em todos os pedidos
# A API requer a chave no cabeçalho 'x-rapidapi-key'
HEADERS = {
    "x-rapidapi-host": settings.API_FOOTBALL_HOST,
    "x-rapidapi-key": settings.API_FOOTBALL_KEY,
}

async def get_api_status() -> Optional[Dict[str, Any]]:
    """
    Faz um pedido ao endpoint /status da API para verificar a conectividade e o estado da subscrição.
    """
    # (O resto da função continua igual)
    if not settings.API_FOOTBALL_KEY:
        print("ERRO: A chave da API-Futebol não está configurada no ficheiro .env")
        return None

    endpoint = "/status"
    url = f"{BASE_URL}{endpoint}"

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=HEADERS)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            print(f"Erro de status HTTP ao chamar a API: {e.response.status_code} - {e.response.text}")
            return None
        except httpx.RequestError as e:
            print(f"Erro de requisição ao chamar a API: {e}")
            return None


async def get_leagues() -> Optional[List[Dict[str, Any]]]:
    """
    Busca a lista de todas as ligas disponíveis na API-Futebol.
    """
    if not settings.API_FOOTBALL_KEY:
        print("ERRO: A chave da API-Futebol não está configurada.")
        return None

    endpoint = "/leagues"
    url = f"{BASE_URL}{endpoint}"

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=HEADERS)
            response.raise_for_status()
            data = response.json()
            return data.get("response", [])
        except httpx.HTTPStatusError as e:
            print(f"Erro de status HTTP: {e.response.status_code} - {e.response.text}")
            return None
        except httpx.RequestError as e:
            print(f"Erro de requisição: {e}")
            return None

# Buscar Equipes
async def get_teams(league_id: int, season: int) -> Optional[List[Dict[str, Any]]]:
    """
    Busca a lista de todas as equipas de uma liga e temporada específicas.
    """
    if not settings.API_FOOTBALL_KEY:
        print("ERRO: A chave da API-Futebol não está configurada.")
        return None

    endpoint = "/teams"
    url = f"{BASE_URL}{endpoint}"
    params = {"league": str(league_id), "season": str(season)}

    async with httpx.AsyncClient() as client:
        try:
            # O tempo limite pode ser aumentado para pedidos que demoram mais
            response = await client.get(url, headers=HEADERS, params=params, timeout=30.0)
            response.raise_for_status()
            data = response.json()
            return data.get("response", [])
        except httpx.HTTPStatusError as e:
            print(f"Erro de status HTTP: {e.response.status_code} - {e.response.text}")
            return None
        except httpx.RequestError as e:
            print(f"Erro de requisição: {e}")
            return None

# Buscar Jogos
async def get_fixtures(league_id: int, season: int) -> Optional[List[Dict[str, Any]]]:
    """
    Busca a lista de todos os jogos de uma liga e temporada específicas.
    """
    if not settings.API_FOOTBALL_KEY:
        print("ERRO: A chave da API-Futebol não está configurada.")
        return None

    endpoint = "/fixtures"
    url = f"{BASE_URL}{endpoint}"
    params = {"league": str(league_id), "season": str(season)}

    # Este pedido pode ser grande, usamos um timeout maior
    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            response = await client.get(url, headers=HEADERS, params=params)
            response.raise_for_status()
            data = response.json()
            return data.get("response", [])
        except httpx.HTTPStatusError as e:
            print(f"Erro de status HTTP ao buscar jogos: {e.response.status_code} - {e.response.text}")
            return None
        except httpx.RequestError as e:
            print(f"Erro de requisição ao buscar jogos: {e}")
            return None

# Futuramente, adicionaremos outras funções aqui...
