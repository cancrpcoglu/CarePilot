"""triage_reports pgvector embedding kolonu

Revision ID: 3af8182ac61a
Revises: e712e32008c5
Create Date: 2026-07-17 21:43:20.383951

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3af8182ac61a'
down_revision: Union[str, None] = 'e712e32008c5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # pgvector uzantısı (Docker imajı pgvector/pgvector:pg16 ile birlikte gelir)
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")
    # Embedding kolonu ORM modeline eklenmez (SQLite testleri için); ham SQL ile yönetilir
    op.execute("ALTER TABLE triage_reports ADD COLUMN embedding vector(3072)")


def downgrade() -> None:
    op.execute("ALTER TABLE triage_reports DROP COLUMN IF EXISTS embedding")
