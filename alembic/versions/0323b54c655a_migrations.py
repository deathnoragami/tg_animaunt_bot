"""migrations

Revision ID: 0323b54c655a
Revises: 03d77590847e
Create Date: 2023-11-29 15:25:19.049813

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0323b54c655a'
down_revision: Union[str, None] = '03d77590847e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Title', sa.Column('complete', sa.Boolean(), nullable=True))
    op.drop_column('Title', 'complite')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Title', sa.Column('complite', sa.BOOLEAN(), nullable=True))
    op.drop_column('Title', 'complete')
    # ### end Alembic commands ###