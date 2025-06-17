import os
from dotenv import load_dotenv
from pathlib import Path

# Constrói o caminho para o arquivo .env na raiz do projeto
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

class Settings:
    # Configurações do JWT
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "default_secret_key_if_not_set")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

# Cria uma instância das configurações para ser usada em toda a aplicação
settings = Settings()
