"""track_table

Revision ID: 5a95fe7fb426
Revises: 
Create Date: 2020-05-27 07:11:56.094943

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5a95fe7fb426'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('track',
    sa.Column('id', sa.String(length=16), nullable=False),
    sa.Column('title', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('track')
    # ### end Alembic commands ###