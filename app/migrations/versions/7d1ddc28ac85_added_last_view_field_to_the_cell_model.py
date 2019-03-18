"""added last view field to the Cell model

Revision ID: 7d1ddc28ac85
Revises: 6cdf42f05327
Create Date: 2019-03-18 06:37:51.177602

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7d1ddc28ac85'
down_revision = '6cdf42f05327'
branch_labels = None
depends_on = None


def upgrade(engine_name):
    globals()["upgrade_%s" % engine_name]()


def downgrade(engine_name):
    globals()["downgrade_%s" % engine_name]()





def upgrade_():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('main_cells', sa.Column('last_view', sa.DateTime(timezone=True), nullable=True))
    # ### end Alembic commands ###


def downgrade_():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('main_cells', 'last_view')
    # ### end Alembic commands ###

