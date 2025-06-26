import os
from dotenv import load_dotenv
from pathlib import Path

# --- INÍCIO DA CORREÇÃO ---
# Constrói o caminho para a raiz do projeto de forma robusta
# __file__ é o caminho para este ficheiro (config.py)
# .resolve().parents[2] sobe dois níveis de diretório (de /app/core/ para /)
# para chegar à raiz do subprojeto 'backend'.
# Para chegar à raiz do projeto principal, subimos 3 níveis.
# __file__ -> .../backend/app/core/config.py
# parents[0] -> .../backend/app/core/
# parents[1] -> .../backend/app/
# parents[2] -> .../backend/
# parents[3] -> .../sportsbet-ev-ai/
PROJECT_ROOT_DIR = Path(__file__).resolve().parents[3]
ENV_PATH = PROJECT_ROOT_DIR / '.env'

# print(f"DEBUG [config.py]: A procurar .env em: {ENV_PATH}") # Para depuração
if ENV_PATH.exists():
    load_dotenv(dotenv_path=ENV_PATH)
    # print("DEBUG [config.py]: .env carregado!")
else:
    print(f"ATENÇÃO [config.py]: Ficheiro .env não encontrado em {ENV_PATH}")
# --- FIM DA CORREÇÃO ---

class Settings:
    # Configurações do JWT
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "default_secret_key_if_not_set")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

    # Chave da API para dados de futebol
    API_FOOTBALL_KEY: str = os.getenv("API_FOOTBALL_KEY")
    API_FOOTBALL_HOST: str = "v3.football.api-sports.io" # O host da API

    # --- NOVA CONFIGURAÇÃO ADICIONADA - GOOGLE AI STUDIO ---
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY")

# Cria uma instância das configurações para ser usada em toda a aplicação
settings = Settings()
