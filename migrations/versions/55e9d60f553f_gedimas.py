"""gedimas

Revision ID: 55e9d60f553f
Revises: bde72a12434f
Create Date: 2022-02-28 14:07:01.688358

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '55e9d60f553f'
down_revision = 'bde72a12434f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('irasas', sa.Column('Gedimas', sa.String(length=200), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('irasas', 'Gedimas')
    # ### end Alembic commands ###
