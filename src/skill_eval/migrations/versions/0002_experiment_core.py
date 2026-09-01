"""Create core experiment persistence tables.

Revision ID: 0002_experiment_core
Revises: 0001_initial_metadata
Create Date: 2026-04-12
"""

from collections.abc import Sequence

import sqlalchemy as sa  # pyright: ignore[reportMissingImports]
from alembic import op  # pyright: ignore[reportMissingImports]

revision: str = "0002_experiment_core"
down_revision: str | None = "0001_initial_metadata"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Create normalized, auditable experiment state."""
    op.create_table(
        "config_snapshot",
        sa.Column("id", sa.Text(), nullable=False),
        sa.Column("sha256", sa.Text(), nullable=False),
        sa.Column("redacted_yaml", sa.Text(), nullable=False),
        sa.Column("created_at", sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("sha256"),
    )
    op.create_table(
        "model",
        sa.Column("id", sa.Text(), nullable=False),
        sa.Column("provider", sa.Text(), nullable=False),
        sa.Column("model_name", sa.Text(), nullable=False),
        sa.Column("settings_json", sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "experiment",
        sa.Column("id", sa.Text(), nullable=False),
        sa.Column("created_at", sa.Text(), nullable=False),
        sa.Column("skill_name", sa.Text(), nullable=False),
        sa.Column("skill_sha256", sa.Text(), nullable=False),
        sa.Column("eval_set_sha256", sa.Text(), nullable=False),
        sa.Column("capability_profile", sa.Text(), nullable=False),
        sa.Column("harness_version", sa.Text(), nullable=False),
        sa.Column("config_snapshot_id", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(["config_snapshot_id"], ["config_snapshot.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "eval_case",
        sa.Column("id", sa.Text(), nullable=False),
        sa.Column("experiment_id", sa.Text(), nullable=False),
        sa.Column("prompt", sa.Text(), nullable=False),
        sa.Column("assertions_json", sa.Text(), nullable=False),
        sa.Column("input_artifacts_json", sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(["experiment_id"], ["experiment.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "condition",
        sa.Column("id", sa.Text(), nullable=False),
        sa.Column("experiment_id", sa.Text(), nullable=False),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("skill_context_json", sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(["experiment_id"], ["experiment.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("experiment_id", "name"),
    )
    op.create_table(
        "skill_snapshot",
        sa.Column("id", sa.Text(), nullable=False),
        sa.Column("experiment_id", sa.Text(), nullable=False),
        sa.Column("parent_snapshot_id", sa.Text(), nullable=True),
        sa.Column("sha256", sa.Text(), nullable=False),
        sa.Column("manifest_json", sa.Text(), nullable=False),
        sa.Column("skill_md", sa.Text(), nullable=False),
        sa.Column("created_at", sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(["experiment_id"], ["experiment.id"]),
        sa.ForeignKeyConstraint(["parent_snapshot_id"], ["skill_snapshot.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "candidate",
        sa.Column("id", sa.Text(), nullable=False),
        sa.Column("experiment_id", sa.Text(), nullable=False),
        sa.Column("source_snapshot_id", sa.Text(), nullable=False),
        sa.Column("candidate_snapshot_id", sa.Text(), nullable=False),
        sa.Column("enhancer_model_id", sa.Text(), nullable=False),
        sa.Column("mode", sa.Text(), nullable=False),
        sa.Column("status", sa.Text(), nullable=False),
        sa.Column("rationale", sa.Text(), nullable=True),
        sa.Column("selection_json", sa.Text(), nullable=True),
        sa.Column("created_at", sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(["experiment_id"], ["experiment.id"]),
        sa.ForeignKeyConstraint(["source_snapshot_id"], ["skill_snapshot.id"]),
        sa.ForeignKeyConstraint(["candidate_snapshot_id"], ["skill_snapshot.id"]),
        sa.ForeignKeyConstraint(["enhancer_model_id"], ["model.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "attempt",
        sa.Column("id", sa.Text(), nullable=False),
        sa.Column("experiment_id", sa.Text(), nullable=False),
        sa.Column("eval_case_id", sa.Text(), nullable=False),
        sa.Column("model_id", sa.Text(), nullable=False),
        sa.Column("condition_id", sa.Text(), nullable=False),
        sa.Column("skill_snapshot_id", sa.Text(), nullable=False),
        sa.Column("candidate_id", sa.Text(), nullable=True),
        sa.Column("repetition", sa.Integer(), nullable=False),
        sa.Column("status", sa.Text(), nullable=False),
        sa.Column("started_at", sa.Text(), nullable=True),
        sa.Column("finished_at", sa.Text(), nullable=True),
        sa.Column("input_tokens", sa.Integer(), nullable=True),
        sa.Column("output_tokens", sa.Integer(), nullable=True),
        sa.Column("cost_usd", sa.Float(), nullable=True),
        sa.Column("duration_ms", sa.Integer(), nullable=True),
        sa.Column("error_json", sa.Text(), nullable=True),
        sa.Column("transcript", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(["experiment_id"], ["experiment.id"]),
        sa.ForeignKeyConstraint(["eval_case_id"], ["eval_case.id"]),
        sa.ForeignKeyConstraint(["model_id"], ["model.id"]),
        sa.ForeignKeyConstraint(["condition_id"], ["condition.id"]),
        sa.ForeignKeyConstraint(["skill_snapshot_id"], ["skill_snapshot.id"]),
        sa.ForeignKeyConstraint(["candidate_id"], ["candidate.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "eval_case_id",
            "model_id",
            "condition_id",
            "skill_snapshot_id",
            "repetition",
        ),
    )
    op.create_table(
        "grade",
        sa.Column("id", sa.Text(), nullable=False),
        sa.Column("attempt_id", sa.Text(), nullable=False),
        sa.Column("grader_id", sa.Text(), nullable=False),
        sa.Column("assertion_id", sa.Text(), nullable=False),
        sa.Column("passed", sa.Integer(), nullable=False),
        sa.Column("score", sa.Float(), nullable=True),
        sa.Column("evidence", sa.Text(), nullable=False),
        sa.CheckConstraint("passed IN (0, 1)"),
        sa.ForeignKeyConstraint(["attempt_id"], ["attempt.id"]),
        sa.ForeignKeyConstraint(["grader_id"], ["model.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "artifact",
        sa.Column("id", sa.Text(), nullable=False),
        sa.Column("attempt_id", sa.Text(), nullable=False),
        sa.Column("path", sa.Text(), nullable=False),
        sa.Column("media_type", sa.Text(), nullable=True),
        sa.Column("sha256", sa.Text(), nullable=False),
        sa.Column("content", sa.LargeBinary(), nullable=False),
        sa.ForeignKeyConstraint(["attempt_id"], ["attempt.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("attempt_by_case", "attempt", ["experiment_id", "eval_case_id"])
    op.create_index(
        "attempt_by_model_condition", "attempt", ["model_id", "condition_id"]
    )
    op.create_index("attempt_by_status", "attempt", ["status"])


def downgrade() -> None:
    """Drop the experiment schema in dependency-safe reverse order."""
    op.drop_index("attempt_by_status", table_name="attempt")
    op.drop_index("attempt_by_model_condition", table_name="attempt")
    op.drop_index("attempt_by_case", table_name="attempt")
    op.drop_table("artifact")
    op.drop_table("grade")
    op.drop_constraint("attempt_candidate_id_fkey", "attempt", type_="foreignkey")
    op.drop_table("candidate")
    op.drop_table("attempt")
    op.drop_table("skill_snapshot")
    op.drop_table("condition")
    op.drop_table("eval_case")
    op.drop_table("experiment")
    op.drop_table("model")
    op.drop_table("config_snapshot")
