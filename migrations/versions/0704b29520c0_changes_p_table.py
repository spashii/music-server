"""changes_p_table

Revision ID: 0704b29520c0
Revises: 
Create Date: 2020-05-29 01:12:19.047721

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0704b29520c0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('playlist',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=32), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('title')
    )
    op.create_table('track',
    sa.Column('id', sa.String(length=16), nullable=False),
    sa.Column('title', sa.String(length=128), nullable=True),
    sa.Column('date_added', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('playlist_tracks',
    sa.Column('playlist_id', sa.Integer(), nullable=True),
    sa.Column('track_id', sa.String(length=16), nullable=True),
    sa.ForeignKeyConstraint(['playlist_id'], ['playlist.id'], ),
    sa.ForeignKeyConstraint(['track_id'], ['track.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('playlist_tracks')
    op.drop_table('track')
    op.drop_table('playlist')
    # ### end Alembic commands ###
