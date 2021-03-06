"""changed title to Eng name and added Thai name

Revision ID: 75b384df0246
Revises: db4befd08536
Create Date: 2019-03-12 12:40:27.142664

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '75b384df0246'
down_revision = 'db4befd08536'
branch_labels = None
depends_on = None


def upgrade(engine_name):
    globals()["upgrade_%s" % engine_name]()


def downgrade(engine_name):
    globals()["downgrade_%s" % engine_name]()





def upgrade_():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('main_institutions', sa.Column('campus', sa.String(length=255), nullable=True))
    op.add_column('main_institutions', sa.Column('name_en', sa.String(length=255), nullable=False))
    op.add_column('main_institutions', sa.Column('name_th', sa.String(length=255), nullable=False))
    op.drop_column('main_institutions', 'title')
    # ### end Alembic commands ###


def downgrade_():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('main_institutions', sa.Column('title', sa.VARCHAR(length=255), autoincrement=False, nullable=False))
    op.drop_column('main_institutions', 'name_th')
    op.drop_column('main_institutions', 'name_en')
    op.drop_column('main_institutions', 'campus')
    # ### end Alembic commands ###

