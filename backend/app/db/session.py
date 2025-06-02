from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from dotenv import load_dotenv
import os

# Caminho para o diretório raiz do projeto (sportsbet-ev-ai)
# __file__ é o caminho para session.py (backend/app/db/session.py)
PROJECT_ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
ENV_PATH = os.path.join(PROJECT_ROOT_DIR, '.env')

# print(f"DEBUG: Tentando carregar .env de: {ENV_PATH}") # Linha de debug
if os.path.exists(ENV_PATH):
    load_dotenv(dotenv_path=ENV_PATH)
    # print("DEBUG: .env carregado com sucesso!") # Linha de debug
else:
    print(f"ATENÇÃO: Arquivo .env não encontrado em {ENV_PATH}")

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

if not SQLALCHEMY_DATABASE_URL:
    raise ValueError("DATABASE_URL não está configurada. Verifique seu arquivo .env na raiz do projeto ou as variáveis de ambiente.")

# print(f"DEBUG: DATABASE_URL a ser usada (sem senha): {SQLALCHEMY_DATABASE_URL[:SQLALCHEMY_DATABASE_URL.find('@')]}...") # Debug

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
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
