"""empty message

Revision ID: a9abb95bc5b8
Revises: 92ee03b0bc3f
Create Date: 2016-08-07 22:17:54.647223

"""

# revision identifiers, used by Alembic.
revision = 'a9abb95bc5b8'
down_revision = '92ee03b0bc3f'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('stockitem',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sku', sa.String(length=255), nullable=True),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('unitprice', sa.Float(), nullable=True),
    sa.Column('quantity', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('stockitem')
    ### end Alembic commands ###