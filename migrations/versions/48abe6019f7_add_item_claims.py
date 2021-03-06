"""add item claims

Revision ID: 48abe6019f7
Revises: 3519117eb69
Create Date: 2013-11-05 23:10:11.000329

"""

# revision identifiers, used by Alembic.
revision = '48abe6019f7'
down_revision = '3519117eb69'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('event_item_claims',
    sa.Column('item_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=True),
    sa.Column('purchased', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['item_id'], ['event_items.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('item_id', 'user_id'),
    sa.UniqueConstraint('item_id','user_id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('event_item_claims')
    ### end Alembic commands ###
