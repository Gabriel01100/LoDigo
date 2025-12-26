from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine

from alembic import context
import asyncio
import os

import sys


# Importar Base y modelos
from app.models.base import Base
import app.models.user_model
import app.models.posts_model
import app.models.school_model

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

# Esto permite acceder a las configuraciones
config = context.config

# Configuración de logs
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadatos de los modelos
target_metadata = Base.metadata


# --------- ASYNC RUNNER ----------
def run_migrations_online():
    """Ejecuta migraciones en modo async."""

    from app.database import engine  # Importá tu AsyncEngine real

    connectable = engine.sync_engine  # ✓ convertir a engine síncrono

    async def do_migrations():
        async with engine.begin() as async_conn:
            await async_conn.run_sync(run_sync_migrations)

    def run_sync_migrations(sync_connection):
        context.configure(
            connection=sync_connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
        )

        with context.begin_transaction():
            context.run_migrations()

    import asyncio
    asyncio.run(do_migrations())


# --------- SYNC RUNNER (No se usa, pero queda por compatibilidad) ----------
def run_migrations_offline():
    """Ejecuta migraciones en modo offline."""
    url = config.get_main_option("sqlalchemy.url")

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
    )

    with context.begin_transaction():
        context.run_migrations()


# Decidir según el modo
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
