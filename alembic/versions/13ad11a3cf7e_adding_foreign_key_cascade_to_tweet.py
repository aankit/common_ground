"""adding foreign key cascade to tweet

Revision ID: 13ad11a3cf7e
Revises: 13a192b37ac3
Create Date: 2014-11-20 01:18:27.207914

"""

# revision identifiers, used by Alembic.
revision = '13ad11a3cf7e'
down_revision = '13a192b37ac3'

from alembic import op
import sqlalchemy as sa


def upgrade():
	op.drop_table('deaduser')
			

def downgrade():
    pass
