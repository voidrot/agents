"""Persist immutable suite and fixture bytes for interrupted-run replay.

Revision ID: 0004_replay_inputs
Revises: 0003_attempt_tool_calls
Create Date: 2026-04-12
"""

from collections.abc import Sequence

import sqlalchemy as sa  # pyright: ignore[reportMissingImports]
from alembic import op  # pyright: ignore[reportMissingImports]

revision: str = "0004_replay_inputs"
down_revision: str | None = "0003_attempt_tool_calls"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Store all inputs needed to recreate a queued attempt after interruption."""
    op.add_column("experiment", sa.Column("suite_yaml", sa.Text(), nullable=True))
    op.add_column(
        "experiment", sa.Column("capability_profile_json", sa.Text(), nullable=True)
    )
    op.create_table(
        "input_artifact",
        sa.Column("id", sa.Text(), nullable=False),
        sa.Column("experiment_id", sa.Text(), nullable=False),
        sa.Column("eval_case_id", sa.Text(), nullable=False),
        sa.Column("path", sa.Text(), nullable=False),
        sa.Column("media_type", sa.Text(), nullable=True),
        sa.Column("sha256", sa.Text(), nullable=False),
        sa.Column("content", sa.LargeBinary(), nullable=False),
        sa.ForeignKeyConstraint(["experiment_id"], ["experiment.id"]),
        sa.ForeignKeyConstraint(["eval_case_id"], ["eval_case.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("eval_case_id", "path"),
    )


def downgrade() -> None:
    """Remove replay-specific state in dependency-safe order."""
    op.drop_table("input_artifact")
    op.drop_column("experiment", "capability_profile_json")
    op.drop_column("experiment", "suite_yaml")
