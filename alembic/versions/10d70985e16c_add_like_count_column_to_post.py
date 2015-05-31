""" add like_count column to Post

Revision ID: 10d70985e16c
Revises: 34eea65b4212
Create Date: 2015-05-30 00:35:55.040265

"""

# revision identifiers, used by Alembic.
revision = '10d70985e16c'
down_revision = '34eea65b4212'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('posts', sa.Column('like_count', sa.Integer))



def downgrade():
    pass
