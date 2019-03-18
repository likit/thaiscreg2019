"""added institution ID field

Revision ID: 3b87e445d430
Revises: 42c6ae6c390e
Create Date: 2019-03-16 10:45:46.444097

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3b87e445d430'
down_revision = '42c6ae6c390e'
branch_labels = None
depends_on = None


def upgrade(engine_name):
    globals()["upgrade_%s" % engine_name]()


def downgrade(engine_name):
    globals()["downgrade_%s" % engine_name]()





def upgrade_():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('main_cells', sa.Column('institution_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'main_cells', 'main_institutions', ['institution_id'], ['id'])
    # ### end Alembic commands ###


def downgrade_():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'main_cells', type_='foreignkey')
    op.drop_column('main_cells', 'institution_id')
    # ### end Alembic commands ###
