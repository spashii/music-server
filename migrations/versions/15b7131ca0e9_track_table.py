"""track_table

Revision ID: 15b7131ca0e9
Revises: 
Create Date: 2020-05-27 02:05:52.798189

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '15b7131ca0e9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('track',
    sa.Column('id', sa.String(length=11), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('filename', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('filename')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('track')
    # ### end Alembic commands ###
