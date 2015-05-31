"""create follower  Table

Revision ID: 4bd5553b8fe4
Revises: 36b7bba43c55
Create Date: 2015-05-15 04:10:13.323833

"""

# revision identifiers, used by Alembic.
revision = '4bd5553b8fe4'
down_revision = '36b7bba43c55'
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