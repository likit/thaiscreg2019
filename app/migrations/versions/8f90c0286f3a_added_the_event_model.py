"""added the event model

Revision ID: 8f90c0286f3a
Revises: 806de03f238d
Create Date: 2019-03-12 19:55:12.544563

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8f90c0286f3a'
down_revision = '806de03f238d'
branch_labels = None
depends_on = None


def upgrade(engine_name):
    globals()["upgrade_%s" % engine_name]()


def downgrade(engine_name):
    globals()["downgrade_%s" % engine_name]()





def upgrade_():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('main_events',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('max_participants', sa.Integer(), nullable=True),
    sa.Column('start', sa.DateTime(timezone=True), nullable=True),
    sa.Column('end', sa.DateTime(timezone=True), nullable=True),
    sa.Column('creator_id', sa.Integer(), nullable=True),
    sa.Column('closed', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['creator_id'], ['main_users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade_():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('main_events')
    # ### end Alembic commands ###
