"""Add a column

Revision ID: 4d3df9f649be
Revises: 
Create Date: 2015-04-30 01:44:05.449846

"""

# revision identifiers, used by Alembic.
revision = '4d3df9f649be'
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
     op.add_column('user', sa.Column('password', sa.String(250)))



def downgrade():
    pass
