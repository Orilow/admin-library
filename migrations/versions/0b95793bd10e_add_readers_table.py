"""Add readers table

Revision ID: 0b95793bd10e
Revises: b5082cb3b1df
Create Date: 2025-05-29 23:56:39.392109

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0b95793bd10e'
down_revision: Union[str, None] = 'b5082cb3b1df'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'readers', 
        sa.Column('id', sa.Integer, primary_key=True), 
        sa.Column("name", sa.String, nullable=False),
        sa.Column("email", sa.String, nullable=False),
        sa.UniqueConstraint("email", name="uq_reader_email")
    );
    
    


def downgrade() -> None:
    op.drop_table("readers")
