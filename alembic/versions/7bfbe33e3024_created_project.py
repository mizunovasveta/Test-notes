"""Created project

Revision ID: 7bfbe33e3024
Revises: 
Create Date: 2024-08-29 15:48:39.581901

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from passlib.context import CryptContext


# revision identifiers, used by Alembic.
revision: str = '7bfbe33e3024'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(), nullable=True),
    sa.Column('hashed_password', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('notes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('description', sa.String(length=100), nullable=True),
    sa.Column('owner_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('notes')
    op.drop_table('users')
    # ### end Alembic commands ###
