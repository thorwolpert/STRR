"""empty message

Revision ID: 420791ae10dc
Revises: e6efc402c14d
Create Date: 2024-07-04 01:40:41.901721

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '420791ae10dc'
down_revision = 'e6efc402c14d'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('event_records', schema=None) as batch_op:
        batch_op.add_column(sa.Column('registration_id', sa.INTEGER(), nullable=True))
        batch_op.create_foreign_key('event_records_registration_id_fkey', 'registrations', ['registration_id'], ['id'])


def downgrade():
    with op.batch_alter_table('event_records', schema=None) as batch_op:
        batch_op.drop_column('registration_id')
