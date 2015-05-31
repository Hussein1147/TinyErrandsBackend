"""create Post Table

Revision ID: 36b7bba43c55
Revises: 55dc13288f08
Create Date: 2015-05-15 02:05:33.308738

"""

# revision identifiers, used by Alembic.
revision = '36b7bba43c55'
down_revision = '55dc13288f08'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy import ForeignKey


def upgrade():
     op.create_table(
        'posts',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('body', sa.String(140)),
        sa.Column('timestamp', sa.DateTime),
        sa.Column('user_id', sa.Integer,ForeignKey('user.id'))

    )

def downgrade():
    op.drop_table('posts')