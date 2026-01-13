"""Add ticker_history table

Revision ID: 001
Revises:
Create Date: 2026-01-14 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create ticker_history table
    op.create_table(
        'ticker_history',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('ticker', sa.String(length=20), nullable=False),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('open', sa.Numeric(precision=20, scale=6), nullable=False),
        sa.Column('high', sa.Numeric(precision=20, scale=6), nullable=False),
        sa.Column('low', sa.Numeric(precision=20, scale=6), nullable=False),
        sa.Column('close', sa.Numeric(precision=20, scale=6), nullable=False),
        sa.Column('volume', sa.Integer(), nullable=False),
        sa.Column('dividends', sa.Numeric(precision=20, scale=6), nullable=True),
        sa.Column('stock_splits', sa.Numeric(precision=20, scale=6), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_ticker_history_id'), 'ticker_history', ['id'], unique=False)
    op.create_index(op.f('ix_ticker_history_ticker'), 'ticker_history', ['ticker'], unique=False)
    op.create_index(op.f('ix_ticker_history_date'), 'ticker_history', ['date'], unique=False)
    op.create_index('idx_ticker_date', 'ticker_history', ['ticker', 'date'], unique=True)


def downgrade() -> None:
    op.drop_index('idx_ticker_date', table_name='ticker_history')
    op.drop_index(op.f('ix_ticker_history_date'), table_name='ticker_history')
    op.drop_index(op.f('ix_ticker_history_ticker'), table_name='ticker_history')
    op.drop_index(op.f('ix_ticker_history_id'), table_name='ticker_history')
    op.drop_table('ticker_history')
