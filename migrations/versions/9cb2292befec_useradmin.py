"""useradmin

Revision ID: 9cb2292befec
Revises: 55e9d60f553f
Create Date: 2022-02-28 14:48:33.130805

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9cb2292befec'
down_revision = '55e9d60f553f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('vartotojas', sa.Column('Admin', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('vartotojas', 'Admin')
    # ### end Alembic commands ###
