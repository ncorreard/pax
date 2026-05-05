"""Change sheet_exercises.multiplicity from Integer to Numeric (float coefficient).

Revision ID: h6i7j8k9l0m1
Revises: g5h6i7j8k9l0
Create Date: 2026-05-05

La multiplicité dans WIMS est un coefficient décimal (ex : 0.3, 0.5, 1.5),
pas un compteur d'essais entier.
"""

import sqlalchemy as sa
from alembic import op

revision = "h6i7j8k9l0m1"
down_revision = "g5h6i7j8k9l0"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column(
        "sheet_exercises",
        "multiplicity",
        type_=sa.Numeric(),
        existing_type=sa.Integer(),
        postgresql_using="multiplicity::numeric",
        server_default="1",
    )


def downgrade() -> None:
    op.alter_column(
        "sheet_exercises",
        "multiplicity",
        type_=sa.Integer(),
        existing_type=sa.Numeric(),
        postgresql_using="multiplicity::integer",
        server_default="1",
    )
