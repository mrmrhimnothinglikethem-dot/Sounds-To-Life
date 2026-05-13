"""Alembic environment configuration for database migrations"""
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
import os
from app.config import settings
from app.database import Base

# This is the Alembic Config object, which provides the values of the [alembic]
# section of the .ini file, as well as other options passed to the command via the
# .ini file and command line flags.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Add your model's MetaData object for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# Other values from the config, defined by the [alembic] section
# and/or passed on the command line argument. They default
# to `None` if nothing is specified.

# Enforce using environment variables instead of hardcoded URLs
def get_sqlalchemy_url():
    """Get database URL from environment"""
    return settings.DATABASE_URL

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = get_sqlalchemy_url()

    context.configure(
        url=configuration["sqlalchemy.url"],
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = get_sqlalchemy_url()

    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

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
