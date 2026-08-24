"""Create the initial application metadata table.

Revision ID: 0001_initial_metadata
Revises:
Create Date: 2026-04-12
"""

from collections.abc import Sequence

import sqlalchemy as sa  # pyright: ignore[reportMissingImports]
from alembic import op  # pyright: ignore[reportMissingImports]

revision: str = "0001_initial_metadata"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Create a stable location for application-level metadata."""
    op.create_table(
        "application_metadata",
        sa.Column("key", sa.Text(), nullable=False),
        sa.Column("value", sa.Text(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("key"),
    )


def downgrade() -> None:
    """Remove the initial metadata table for developer-only rollback."""
    op.drop_table("application_metadata")
