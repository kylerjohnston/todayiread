"""empty message

Revision ID: 9810a7d0b422
Revises: None
Create Date: 2016-02-22 18:00:33.429377

"""

# revision identifiers, used by Alembic.
revision = '9810a7d0b422'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('registration_date', sa.DateTime(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'registration_date')
    ### end Alembic commands ###
