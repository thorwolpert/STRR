"""empty message

Revision ID: 430550e80de4
Revises: 55b9517ed210
Create Date: 2024-12-20 01:02:32.526849

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '430550e80de4'
down_revision = '55b9517ed210'
branch_labels = None
depends_on = None


old_options = ('APPLICATION_SUBMITTED', 'INVOICE_GENERATED', 'PAYMENT_COMPLETE', 'PENDING_AUTO_APPROVAL_PROCESSING', 'AUTO_APPROVAL_FULL_REVIEW', 'AUTO_APPROVAL_PROVISIONAL', 'AUTO_APPROVAL_APPROVED', 'FULL_REVIEW_IN_PROGRESS', 'MANUALLY_APPROVED', 'MANUALLY_DENIED', 'MORE_INFORMATION_REQUESTED', 'REGISTRATION_CREATED', 'CERTIFICATE_ISSUED', 'EXPIRED', 'NON_COMPLIANCE_SUSPENDED')
new_options = ('APPLICATION_SUBMITTED', 'INVOICE_GENERATED', 'PAYMENT_COMPLETE', 'PENDING_AUTO_APPROVAL_PROCESSING', 'AUTO_APPROVAL_FULL_REVIEW', 'AUTO_APPROVAL_PROVISIONAL', 'AUTO_APPROVAL_APPROVED', 'FULL_REVIEW_IN_PROGRESS', 'MANUALLY_APPROVED', 'MANUALLY_DENIED', 'MORE_INFORMATION_REQUESTED', 'REGISTRATION_CREATED', 'CERTIFICATE_ISSUED', 'REGISTRATION_EXPIRED', 'NON_COMPLIANCE_SUSPENDED', 'REGISTRATION_CANCELLED')

old_type = sa.Enum(*old_options, name='eventname')
new_type = sa.Enum(*new_options, name='eventname')


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute('ALTER TYPE eventname RENAME TO tmp_eventname')
    new_type.create(op.get_bind())
    op.execute('ALTER TABLE events ALTER COLUMN event_name TYPE eventname USING event_name::text::eventname')
    op.execute('DROP TYPE tmp_eventname')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute('ALTER TYPE eventname RENAME TO tmp_eventname')
    old_type.create(op.get_bind())
    op.execute('ALTER TABLE events ALTER COLUMN event_name TYPE eventname USING event_name::text::eventname')
    op.execute('DROP TYPE tmp_eventname')
    # ### end Alembic commands ###