"""hastaya telefon ve email eklendi

Revision ID: b1c2d3e4f5a6
Revises: 3af8182ac61a
Create Date: 2026-08-01 15:10:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b1c2d3e4f5a6'
down_revision: Union[str, None] = '3af8182ac61a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Nullable kolonlar: mevcut hastaları bozmaz, backfill gerekmez.
    op.add_column('patients', sa.Column('phone', sa.String(length=32), nullable=True))
    op.add_column('patients', sa.Column('email', sa.String(length=255), nullable=True))


def downgrade() -> None:
    op.drop_column('patients', 'email')
    op.drop_column('patients', 'phone')
