from logging.config import fileConfig

from sqlalchemy import pool
from alembic import context

from src.database import metadata, engine
from src.config import settings

# Importa todos os modelos para o metadata ficar populado
import src.models  # noqa: F401

config = context.config

# Sobrescreve a URL do alembic.ini com a do settings
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL.replace("+aiosqlite", ""))

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = metadata


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    with engine.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
