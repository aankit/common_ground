"""create account table

Revision ID: 3270a192245a
Revises: None
Create Date: 2014-11-17 16:35:28.980775

"""

# revision identifiers, used by Alembic.
revision = '3270a192245a'
down_revision = None

from alembic import op
import sqlalchemy as sa

def upgrade():
	op.alter_column('hashtag', 'tweet_id', type_=sa.String(100))


def downgrade():
    pass
