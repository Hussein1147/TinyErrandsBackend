"""add post,about_me last_seen  Table

Revision ID: 34eea65b4212
Revises: 4bd5553b8fe4
Create Date: 2015-05-15 07:24:17.650688

"""

# revision identifiers, used by Alembic.
revision = '34eea65b4212'
down_revision = '4bd5553b8fe4'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('user', sa.Column('about_me', sa.String(250), unique=True))
   
    op.add_column('user', sa.Column('last_seen', sa.DateTime))
    


def downgrade():
    pass
