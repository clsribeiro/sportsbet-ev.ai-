"""add_leagues_table

Revision ID: cd171dd262f6
Revises: ce2b2f4f4dcb
Create Date: 2025-06-23 22:16:05.690205

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cd171dd262f6'
down_revision: Union[str, None] = 'ce2b2f4f4dcb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('leagues',
    sa.Column('id', sa.Integer(), nullable=False, comment='O ID da liga na API-Futebol'),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('country', sa.String(length=100), nullable=False),
    sa.Column('logo', sa.String(length=255), nullable=True),
    sa.Column('type', sa.String(length=50), nullable=True),
    sa.Column('is_sync_enabled', sa.Boolean(), nullable=False, comment='Flag para controlar se sincronizamos equipas e jogos desta liga'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_leagues_name'), 'leagues', ['name'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_leagues_name'), table_name='leagues')
    op.drop_table('leagues')
    # ### end Alembic commands ###
