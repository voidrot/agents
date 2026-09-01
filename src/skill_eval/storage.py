"""SQLite startup, Alembic migration, and backup helpers."""

# pyright: reportMissingImports=false
from __future__ import annotations

import sqlite3
from datetime import UTC, datetime
from pathlib import Path

from alembic import command  # pyright: ignore[reportMissingImports]
from alembic.config import Config  # pyright: ignore[reportMissingImports]
from alembic.runtime.migration import (
    MigrationContext,  # pyright: ignore[reportMissingImports]
)
from alembic.script import ScriptDirectory  # pyright: ignore[reportMissingImports]
from sqlalchemy import create_engine, event  # pyright: ignore[reportMissingImports]
from sqlalchemy.engine import URL, Connection  # pyright: ignore[reportMissingImports]
from sqlalchemy.exc import SQLAlchemyError  # pyright: ignore[reportMissingImports]


class DatabaseMigrationError(RuntimeError):
    """Raised when an automatic schema migration cannot complete safely."""


def _sqlite_url(path: Path) -> URL:
    return URL.create("sqlite+pysqlite", database=str(path.resolve()))


def _migration_config(url: URL) -> Config:
    config = Config()
    config.set_main_option("script_location", str(Path(__file__).parent / "migrations"))
    config.set_main_option("sqlalchemy.url", url.render_as_string(hide_password=True))
    return config


def _configure_sqlite(connection: sqlite3.Connection, _record: object) -> None:
    connection.execute("PRAGMA foreign_keys = ON")
    connection.execute("PRAGMA busy_timeout = 30000")


def _head_revision(config: Config) -> str | None:
    return ScriptDirectory.from_config(config).get_current_head()


def migrate_database(path: Path) -> str | None:
    """Upgrade a SQLite database to the packaged Alembic head.

    Startup takes a SQLite write lock before invoking Alembic so independent CLI
    invocations cannot simultaneously alter the schema. Any error is rolled
    back and reported with the current/head revision context.
    """
    path = path.expanduser()
    path.parent.mkdir(parents=True, exist_ok=True)
    url = _sqlite_url(path)
    engine = create_engine(url, future=True)
    event.listen(engine, "connect", _configure_sqlite)
    config = _migration_config(url)

    try:
        with engine.connect() as connection:
            _enable_wal(connection)
            connection.exec_driver_sql("BEGIN IMMEDIATE")
            config.attributes["connection"] = connection
            before = MigrationContext.configure(connection).get_current_revision()
            before_display = before if before is not None else "unversioned"
            required = _head_revision(config)
            required_display = required if required is not None else "none"
            try:
                command.upgrade(config, "head")
                revision = MigrationContext.configure(connection).get_current_revision()
                connection.commit()
                return revision
            except Exception as error:
                connection.rollback()
                raise DatabaseMigrationError(
                    "database migration failed "
                    f"(current revision={before_display}, required={required_display}): {error}"
                ) from error
    except DatabaseMigrationError:
        raise
    except SQLAlchemyError as error:
        raise DatabaseMigrationError(
            f"could not initialize database {path}: {error}"
        ) from error
    finally:
        engine.dispose()


def _enable_wal(connection: Connection) -> None:
    """Enable WAL for on-disk databases before applying migrations."""
    connection.exec_driver_sql("PRAGMA journal_mode = WAL")


def database_status(path: Path) -> tuple[str | None, str | None]:
    """Return the current and packaged Alembic revisions without altering data."""
    url = _sqlite_url(path)
    engine = create_engine(url, future=True)
    event.listen(engine, "connect", _configure_sqlite)
    config = _migration_config(url)
    try:
        with engine.connect() as connection:
            current = MigrationContext.configure(connection).get_current_revision()
            return current, _head_revision(config)
    finally:
        engine.dispose()


def backup_database(path: Path, destination: Path | None = None) -> Path:
    """Create a consistent SQLite backup using SQLite's native backup API."""
    path = path.expanduser()
    if not path.exists():
        raise DatabaseMigrationError(f"database does not exist: {path}")

    if destination is None:
        timestamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
        destination = path.with_name(f"{path.stem}-{timestamp}.backup{path.suffix}")
    destination = destination.expanduser()
    destination.parent.mkdir(parents=True, exist_ok=True)

    try:
        with sqlite3.connect(path) as source, sqlite3.connect(destination) as target:
            source.backup(target)
    except sqlite3.Error as error:
        raise DatabaseMigrationError(
            f"could not back up database {path}: {error}"
        ) from error
    return destination


def backup_before_non_transactional_migration(path: Path) -> Path:
    """Reserved migration hook for future SQLite table-copy revisions."""
    return backup_database(path)
