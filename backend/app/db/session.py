from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from dotenv import load_dotenv
import os
from urllib.parse import quote_plus

# Caminho para o diretório raiz do projeto (sportsbet-ev-ai)
PROJECT_ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
ENV_PATH = os.path.join(PROJECT_ROOT_DIR, '.env')

# print(f"DEBUG: Tentando carregar .env de: {ENV_PATH}")
if os.path.exists(ENV_PATH):
    load_dotenv(dotenv_path=ENV_PATH)
    # print("DEBUG: .env carregado com sucesso!")
else:
    print(f"ATENÇÃO: Arquivo .env não encontrado em {ENV_PATH}")

# Carrega as variáveis individuais do banco de dados
DB_USER = os.getenv("DB_USER")
RAW_DB_PASSWORD = os.getenv("DB_PASSWORD") # Renomeado para clareza
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

if not all([DB_USER, RAW_DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME]):
    raise ValueError("Uma ou mais variáveis de configuração do banco de dados (DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME) não estão definidas.")

# Codifica a senha para uso seguro na URL
ENCODED_DB_PASSWORD = quote_plus(RAW_DB_PASSWORD)

# Constrói a SQLALCHEMY_DATABASE_URL com a senha codificada
SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{ENCODED_DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# print(f"DEBUG: DATABASE_URL construída: {SQLALCHEMY_DATABASE_URL.replace(DB_PASSWORD, '********')}") # Debug, ocultando a senha

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=False) # echo=True para debug SQL

AsyncSessionLocal = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False
)

from app.db.base_class import Base # Importa a Base

async def get_db_session():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit() # Commit aqui pode ser muito agressivo, geralmente o commit é feito no service layer
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
