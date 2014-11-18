"""drop friend column

Revision ID: 3bee4963f9fc
Revises: 3270a192245a
Create Date: 2014-11-18 00:18:02.282922

"""

# revision identifiers, used by Alembic.
revision = '3bee4963f9fc'
down_revision = '3270a192245a'

from alembic import op
import sqlalchemy as sa


def upgrade():
	op.drop_column('friend', 'friend')

def downgrade():
    pass
