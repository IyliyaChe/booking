"""‘Change’

Revision ID: e87fb195563c
Revises: 45413aa80d36
Create Date: 2024-10-09 10:31:34.120309

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e87fb195563c'
down_revision: Union[str, None] = '45413aa80d36'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('hotels', sa.Column('location', sa.String(), nullable=False))
    op.drop_column('hotels', 'locaton')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('hotels', sa.Column('locaton', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_column('hotels', 'location')
    # ### end Alembic commands ###