from logging.config import fileConfig

from sqlalchemy import engine_from_config # Mantido do original, mas não usaremos para URL
from sqlalchemy import pool
from sqlalchemy import create_engine # Adicionado para criar engine com URL do .env

from alembic import context

# --- Início das Nossas Modificações ---
import os
from dotenv import load_dotenv
from urllib.parse import quote_plus # Para codificar a senha

# Caminho para o diretório raiz do projeto (sportsbet-ev-ai) onde o .env está
PROJECT_ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ENV_PATH = os.path.join(PROJECT_ROOT_DIR, '.env')

# print(f"DEBUG [Alembic env.py]: Tentando carregar .env de: {ENV_PATH}")
if os.path.exists(ENV_PATH):
    load_dotenv(dotenv_path=ENV_PATH)
    # print("DEBUG [Alembic env.py]: .env carregado com sucesso!")
else:
    print(f"ATENÇÃO [Alembic env.py]: Arquivo .env não encontrado em {ENV_PATH}")

# Importe a Base dos seus modelos SQLAlchemy
from app.db.base_class import Base

# IMPORTANTE: Importe todos os seus módulos de modelos aqui.
import app.models.user
import app.models.role
import app.models.permission
import app.models.user_feature_preference
# --- Fim das Nossas Modificações (na seção de imports e setup inicial) ---

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# --- INÍCIO DA NOSSA LINHA DE DEBUG ---
print("--- Tabelas detetadas pelo Alembic ---")
print(Base.metadata.tables.keys())
print("------------------------------------")
# --- FIM DA NOSSA LINHA DE DEBUG ---

target_metadata = Base.metadata

def get_database_url_sync():
    """Constrói a URL de conexão síncrona a partir das variáveis de ambiente, codificando a senha."""
    db_user = os.getenv("DB_USER")
    raw_db_password = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")
    db_name = os.getenv("DB_NAME")

    if not all([db_user, raw_db_password, db_host, db_port, db_name]):
        raise ValueError(
            "Variáveis de ambiente DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME "
            "não estão todas configuradas para Alembic. Verifique o .env."
        )
    
    # Codifica a senha para uso seguro em URLs
    encoded_db_password = quote_plus(raw_db_password)

    url = f"postgresql://{db_user}:{encoded_db_password}@{db_host}:{db_port}/{db_name}"
    # print(f"DEBUG [Alembic get_database_url_sync]: URL: {url.replace(encoded_db_password, '********')}")
    return url

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.
    """
    url = get_database_url_sync() # Usa a função corrigida
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.
    """
    sync_db_url = get_database_url_sync() # Usa a função corrigida
    connectable = create_engine(sync_db_url, poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
