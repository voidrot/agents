"""Persist immutable bundled skill resources for replay.

Revision ID: 0005_skill_resources
Revises: 0004_replay_inputs
Create Date: 2026-04-12
"""

from collections.abc import Sequence

import sqlalchemy as sa  # pyright: ignore[reportMissingImports]
from alembic import op  # pyright: ignore[reportMissingImports]

revision: str = "0005_skill_resources"
down_revision: str | None = "0004_replay_inputs"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Store each regular skill file once per immutable snapshot."""
    op.create_table(
        "skill_resource",
        sa.Column("id", sa.Text(), nullable=False),
        sa.Column("skill_snapshot_id", sa.Text(), nullable=False),
        sa.Column("path", sa.Text(), nullable=False),
        sa.Column("media_type", sa.Text(), nullable=True),
        sa.Column("sha256", sa.Text(), nullable=False),
        sa.Column("content", sa.LargeBinary(), nullable=False),
        sa.ForeignKeyConstraint(["skill_snapshot_id"], ["skill_snapshot.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("skill_snapshot_id", "path"),
    )


def downgrade() -> None:
    """Remove stored skill-resource blobs."""
    op.drop_table("skill_resource")
