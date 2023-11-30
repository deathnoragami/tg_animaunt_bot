"""migrations

Revision ID: 1fe077b93ae4
Revises: 0323b54c655a
Create Date: 2023-11-29 19:07:02.183950

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1fe077b93ae4'
down_revision: Union[str, None] = '0323b54c655a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Title', sa.Column('remote_path', sa.String(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Title', 'remote_path')
    # ### end Alembic commands ###
