"""Add search and sort indices

Revision ID: 2b707ec995f7
Revises: 269514c7d861
Create Date: 2024-07-19 11:03:26.021314

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '2b707ec995f7'
down_revision = '269514c7d861'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('addresses', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_addresses_city'), ['city'], unique=False)
        batch_op.create_index(batch_op.f('ix_addresses_street_address'), ['street_address'], unique=False)

    with op.batch_alter_table('registrations', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_registrations_status'), ['status'], unique=False)
        batch_op.create_index(batch_op.f('ix_registrations_submission_date'), ['submission_date'], unique=False)

    op.execute(
        """
        CREATE INDEX ix_contacts_fullname ON contacts (
            (firstname || ' ' || lastname)
        );
        """
    )


def downgrade():
    with op.batch_alter_table('addresses', schema=None) as batch_op:
        op.drop_index('ix_addresses_street_address')
        op.drop_index('ix_addresses_city')

    with op.batch_alter_table('registrations', schema=None) as batch_op:
        op.drop_index('ix_registrations_submission_date')
        op.drop_index('ix_registrations_status')

    op.execute('DROP INDEX ix_contacts_fullname;')
