"""Add description to books

Revision ID: 9ef89beedff9
Revises: e724129ad93d
Create Date: 2025-05-30 21:06:40.253423

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9ef89beedff9'
down_revision: Union[str, None] = 'e724129ad93d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('books', sa.Column('description', sa.Text(), nullable=True))
    op.execute("UPDATE books SET description = 'Здесь будет описание, но пока здесь пусто...'")
    op.alter_column('books', 'description', nullable=False)


def downgrade():
    op.drop_column('books', 'description')
