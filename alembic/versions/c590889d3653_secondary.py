"""Secondary

Revision ID: c590889d3653
Revises: 6f62921b13f1
Create Date: 2026-04-16 18:30:24.835353

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c590889d3653'
down_revision: Union[str, None] = '6f62921b13f1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
        op.execute("""
        CREATE INDEX IF NOT EXISTS chunk_embedding_ivfflat_idx
        ON chunks
        USING ivfflat (embedding vector_cosine_ops)
        WITH (lists = 10)
    """)


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS chunk_embedding_ivfflat_idx")
