"""add ivfflat index on chunk embedding

Revision ID: 743de3fbb972
Revises: 7003814cb191
Create Date: 2026-04-07 07:11:20.640048

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '743de3fbb972'
down_revision: Union[str, None] = '7003814cb191'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade():
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")
    op.execute("""
        CREATE INDEX IF NOT EXISTS chunk_embedding_ivfflat_idx
        ON chunks
        USING ivfflat (embedding vector_cosine_ops)
        WITH (lists = 100)
    """)


def downgrade():
    op.execute("DROP INDEX IF EXISTS chunk_embedding_ivfflat_idx")
