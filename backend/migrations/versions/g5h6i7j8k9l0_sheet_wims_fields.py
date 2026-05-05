"""Add WIMS-compatible fields to sheets and sheet_exercises.

Revision ID: g5h6i7j8k9l0
Revises: f4a5b6c7d8e9
Create Date: 2026-05-05

sheets       : author, keywords, level, domain, status
sheet_exercises: points, multiplicity, prerequisite, active
"""

import sqlalchemy as sa
from alembic import op

revision = "g5h6i7j8k9l0"
down_revision = "f4a5b6c7d8e9"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # sheets
    op.add_column("sheets", sa.Column("author",   sa.String(200),          nullable=True))
    op.add_column("sheets", sa.Column("keywords", sa.ARRAY(sa.String()),   nullable=True))
    op.add_column("sheets", sa.Column("level",    sa.String(10),           nullable=True))
    op.add_column("sheets", sa.Column("domain",   sa.String(100),          nullable=True))
    # 0 = caché, 1 = visible (scoré), 3 = visible non scoré (testez-vous)
    op.add_column("sheets", sa.Column("status",   sa.SmallInteger(),       nullable=False,
                                      server_default="1"))

    # sheet_exercises
    op.add_column("sheet_exercises", sa.Column("points",       sa.Integer(),    nullable=False,
                                               server_default="10"))
    op.add_column("sheet_exercises", sa.Column("multiplicity", sa.Integer(),    nullable=False,
                                               server_default="1"))
    op.add_column("sheet_exercises", sa.Column("prerequisite", sa.String(100),  nullable=True))
    op.add_column("sheet_exercises", sa.Column("active",       sa.Boolean(),    nullable=False,
                                               server_default="true"))


def downgrade() -> None:
    for col in ("active", "prerequisite", "multiplicity", "points"):
        op.drop_column("sheet_exercises", col)
    for col in ("status", "domain", "level", "keywords", "author"):
        op.drop_column("sheets", col)
