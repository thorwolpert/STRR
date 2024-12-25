"""empty message

Revision ID: ed33e07431ea
Revises: a5de00ec274f
Create Date: 2024-07-06 21:00:00.640431

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'ed33e07431ea'
down_revision = 'a5de00ec274f'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('terms_of_use_accepted')


def downgrade():
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('terms_of_use_accepted', sa.BOOLEAN(), nullable=False, server_default='false'))
