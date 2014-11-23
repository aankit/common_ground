"""remove deaduser

Revision ID: 243b9e344410
Revises: 13ad11a3cf7e
Create Date: 2014-11-20 10:45:20.276897

"""

# revision identifiers, used by Alembic.
revision = '243b9e344410'
down_revision = '13ad11a3cf7e'

from alembic import op
import sqlalchemy as sa


def upgrade():
	op.drop_table('deaduser')
	op.create_table(
			'nouser',
			 sa.Column('id', sa.Integer, primary_key=True),
			 sa.Column('user_id', sa.Integer, sa.ForeignKey('user.id'), nullable=False)
			 )

def downgrade():
    pass
