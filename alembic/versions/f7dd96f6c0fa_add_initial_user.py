"""Add initial user

Revision ID: f7dd96f6c0fa
Revises: 7bfbe33e3024
Create Date: 2024-08-29 16:58:40.229446

"""
from typing import Sequence, Union

from alembic import op
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from models import User


# revision identifiers, used by Alembic.
revision: str = 'f7dd96f6c0fa'
down_revision: Union[str, None] = '7bfbe33e3024'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def upgrade():
    bind = op.get_bind()
    session = Session(bind=bind)

    hashed_password = pwd_context.hash("your_password")
    new_user = User(username="your_username", hashed_password=hashed_password)
    session.add(new_user)
    session.commit()

def downgrade():
    bind = op.get_bind()
    session = Session(bind=bind)

    session.query(User).filter_by(username="your_username").delete()
    session.commit()
