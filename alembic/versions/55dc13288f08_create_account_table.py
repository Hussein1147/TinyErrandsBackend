
"""create account table

Revision ID: 55dc13288f08
Revises: 4d3df9f649be
Create Date: 2015-05-13 00:05:46.097549

"""

# revision identifiers, used by Alembic.
revision = '55dc13288f08'
down_revision = '4d3df9f649be'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy import Column,ForeignKey,Integer,BigInteger,String



def upgrade():
    
    op.create_table(
        'followers',
        sa.Column('follower_id', sa.Integer, ForeignKey('user.id')),
        sa.Column('followed_id', sa.Integer, ForeignKey('user.id')),
    )

def downgrade():
    op.drop_table('followers')