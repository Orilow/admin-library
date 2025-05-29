"""Update books table to match requirements

Revision ID: b5082cb3b1df
Revises: c4b311fb2d36
Create Date: 2025-05-29 21:42:36.619425

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b5082cb3b1df'
down_revision: Union[str, None] = 'c4b311fb2d36'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.drop_column('books', 'description')
    op.add_column('books', sa.Column('year_published', sa.Integer, nullable=True))
    op.add_column('books', sa.Column('isbn', sa.String, nullable=True))
    op.add_column('books', sa.Column('copies_available', sa.Integer, nullable=False, server_default='1'))
    op.create_unique_constraint('uq_isbn', 'books', ['isbn'])
    op.create_check_constraint('check_copies_available', 'books', 'copies_available >= 0')
    op.alter_column('books', 'title', nullable=False)
    op.alter_column('books', 'author', nullable=False)


def downgrade():
    op.drop_constraint('check_copies_available', 'books', type_='check')
    op.drop_constraint('uq_isbn', 'books', type_='unique')
    op.drop_column('books', 'copies_available')
    op.drop_column('books', 'isbn')
    op.drop_column('books', 'year_published')
    op.add_column('books', sa.Column('description', sa.String, nullable=True))
    op.alter_column('books', 'title', nullable=True)
    op.alter_column('books', 'author', nullable=True)
