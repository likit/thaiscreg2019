"""added the venue field to the event model

Revision ID: 9cc9eed43339
Revises: 8f90c0286f3a
Create Date: 2019-03-12 19:56:52.402834

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9cc9eed43339'
down_revision = '8f90c0286f3a'
branch_labels = None
depends_on = None


def upgrade(engine_name):
    globals()["upgrade_%s" % engine_name]()


def downgrade(engine_name):
    globals()["downgrade_%s" % engine_name]()





def upgrade_():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('main_events', sa.Column('venue', sa.String(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade_():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('main_events', 'venue')
    # ### end Alembic commands ###
