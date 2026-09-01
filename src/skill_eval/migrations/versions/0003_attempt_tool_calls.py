"""Record normalized tool-call counts for each execution attempt.

Revision ID: 0003_attempt_tool_calls
Revises: 0002_experiment_core
Create Date: 2026-04-12
"""

from collections.abc import Sequence

import sqlalchemy as sa  # pyright: ignore[reportMissingImports]
from alembic import op  # pyright: ignore[reportMissingImports]

revision: str = "0003_attempt_tool_calls"
down_revision: str | None = "0002_experiment_core"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Add a nullable counter so historical attempts remain valid."""
    op.add_column("attempt", sa.Column("tool_calls", sa.Integer(), nullable=True))


def downgrade() -> None:
    """Remove the normalized tool-call metric."""
    op.drop_column("attempt", "tool_calls")
