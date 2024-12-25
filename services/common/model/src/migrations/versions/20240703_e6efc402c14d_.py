"""empty message

Revision ID: e6efc402c14d
Revises: aa4d983f79c4
Create Date: 2024-07-03 23:56:09.200319

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'e6efc402c14d'
down_revision = 'aa4d983f79c4'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('terms_of_use_accepted', sa.BOOLEAN(), nullable=False, server_default='false'))

    with op.batch_alter_table('event_records', schema=None) as batch_op:
        batch_op.add_column(sa.Column('visible_to_end_user', sa.BOOLEAN(), nullable=False, server_default='false'))


def downgrade():
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('terms_of_use_accepted')

    with op.batch_alter_table('event_records', schema=None) as batch_op:
        batch_op.drop_column('visible_to_end_user')
