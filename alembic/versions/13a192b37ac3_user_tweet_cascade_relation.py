"""user tweet cascade relation

Revision ID: 13a192b37ac3
Revises: 21be8f29d918
Create Date: 2014-11-19 21:49:29.100958

"""

# revision identifiers, used by Alembic.
revision = '13a192b37ac3'
down_revision = '21be8f29d918'

from alembic import op
import sqlalchemy as sa


def upgrade():
	op.add_column('user', sa.Column('botscore', sa.Integer))

def downgrade():
	op.drop_column('user', 'botscore')
