"""Alembic environment for skill-eval's SQLite database."""

from __future__ import annotations

from alembic import context  # pyright: ignore[reportMissingImports]
from sqlalchemy import engine_from_config, pool  # pyright: ignore[reportMissingImports]
from sqlalchemy.engine import Connection  # pyright: ignore[reportMissingImports]

config = context.config
target_metadata = None


def run_migrations_offline() -> None:
    """Run migrations without a live database connection."""
    context.configure(
        url=config.get_main_option("sqlalchemy.url"),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def _run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations using the startup-owned connection when supplied."""
    connection = config.attributes.get("connection")
    if connection is not None:
        _run_migrations(connection)
        return

    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        _run_migrations(connection)


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
