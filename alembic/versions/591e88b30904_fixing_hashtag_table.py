"""fixing hashtag table

Revision ID: 591e88b30904
Revises: 243b9e344410
Create Date: 2014-11-21 21:50:16.226172

"""

# revision identifiers, used by Alembic.
revision = '591e88b30904'
down_revision = '243b9e344410'

from alembic import op
import sqlalchemy as sa


def upgrade():
	op.drop_column('hashtag', 'user_id')
	op.drop_column('hashtag', 'tweet_id')

def downgrade():
    pass
