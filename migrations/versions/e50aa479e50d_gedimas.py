"""gedimas

Revision ID: e50aa479e50d
Revises: 9cb2292befec
Create Date: 2022-02-28 20:24:10.767569

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e50aa479e50d'
down_revision = '9cb2292befec'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('car',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('Sukurta', sa.DateTime(), nullable=True),
    sa.Column('Modelis', sa.String(length=200), nullable=False),
    sa.Column('Markė', sa.String(length=200), nullable=False),
    sa.Column('Metai', sa.Integer(), nullable=False),
    sa.Column('Variklis', sa.String(length=200), nullable=False),
    sa.Column('Valstybinis numeris', sa.String(length=200), nullable=False),
    sa.Column('VIN', sa.String(length=17), nullable=False),
    sa.Column('vartotojas_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['vartotojas_id'], ['vartotojas.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('gedimas',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('Gedimas', sa.String(length=200), nullable=True),
    sa.Column('masina_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['masina_id'], ['car.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('irasas')
    op.drop_column('vartotojas', 'Admin')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('vartotojas', sa.Column('Admin', sa.BOOLEAN(), nullable=True))
    op.create_table('irasas',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('Sukurta', sa.DATETIME(), nullable=True),
    sa.Column('Modelis', sa.VARCHAR(length=200), nullable=False),
    sa.Column('Markė', sa.VARCHAR(length=200), nullable=False),
    sa.Column('Metai', sa.INTEGER(), nullable=False),
    sa.Column('Variklis', sa.VARCHAR(length=200), nullable=False),
    sa.Column('Valstybinis numeris', sa.VARCHAR(length=200), nullable=False),
    sa.Column('VIN', sa.VARCHAR(length=17), nullable=False),
    sa.Column('vartotojas_id', sa.INTEGER(), nullable=True),
    sa.Column('Gedimas', sa.VARCHAR(length=200), nullable=True),
    sa.ForeignKeyConstraint(['vartotojas_id'], ['vartotojas.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('gedimas')
    op.drop_table('car')
    # ### end Alembic commands ###
