"""migrations

Revision ID: 03d77590847e
Revises: 26601755e951
Create Date: 2023-11-29 14:29:59.658823

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '03d77590847e'
down_revision: Union[str, None] = '26601755e951'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Title', sa.Column('complite', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Title', 'complite')
    # ### end Alembic commands ###
