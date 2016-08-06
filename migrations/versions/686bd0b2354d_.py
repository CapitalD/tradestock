"""empty message

Revision ID: 686bd0b2354d
Revises: None
Create Date: 2016-08-06 22:41:45.020243

"""

# revision identifiers, used by Alembic.
revision = '686bd0b2354d'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('job',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('job')
    ### end Alembic commands ###