"""add wishlists

Revision ID: 3519117eb69
Revises: 3d943ee3b4e
Create Date: 2013-11-03 14:10:07.861337

"""

# revision identifiers, used by Alembic.
revision = '3519117eb69'
down_revision = '3d943ee3b4e'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('event_items',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('cost', sa.Float(), nullable=True),
    sa.Column('quantity', sa.Integer(), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.Column('url', sa.String(length=255), nullable=True),
    sa.Column('event_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['event_id', 'user_id'], ['event_recipients.event_id', 'event_recipients.recipient_id'], name='fk_wishlist', use_alter=True),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('event_items')
    ### end Alembic commands ###
