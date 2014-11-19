"""change friend/friend_id to String from Integer

Revision ID: 21be8f29d918
Revises: 3bee4963f9fc
Create Date: 2014-11-19 15:58:01.836177

"""

# revision identifiers, used by Alembic.
revision = '21be8f29d918'
down_revision = '3bee4963f9fc'

from alembic import op
import sqlalchemy as sa


def upgrade():
	op.alter_column('friend', 'friend_id', type_=sa.String(50))


def downgrade():
    pass
