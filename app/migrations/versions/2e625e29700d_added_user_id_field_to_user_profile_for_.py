"""added user id field to user profile for a relationship

Revision ID: 2e625e29700d
Revises: 75b384df0246
Create Date: 2019-03-12 12:46:17.458362

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2e625e29700d'
down_revision = '75b384df0246'
branch_labels = None
depends_on = None


def upgrade(engine_name):
    globals()["upgrade_%s" % engine_name]()


def downgrade(engine_name):
    globals()["downgrade_%s" % engine_name]()





def upgrade_():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('main_user_profiles', sa.Column('user_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'main_user_profiles', 'main_users', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade_():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'main_user_profiles', type_='foreignkey')
    op.drop_column('main_user_profiles', 'user_id')
    # ### end Alembic commands ###

