"""empty message

Revision ID: b9681cffdca0
Revises: 430550e80de4
Create Date: 2024-12-20 01:13:41.003386

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b9681cffdca0'
down_revision = '430550e80de4'
branch_labels = None
depends_on = None


old_options = ('ACTIVE', 'EXPIRED', 'SUSPENDED')
new_options = ('ACTIVE', 'EXPIRED', 'SUSPENDED', 'CANCELLED')

old_type = sa.Enum(*old_options, name='registrationstatus')
new_type = sa.Enum(*new_options, name='registrationstatus')


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute('ALTER TYPE registrationstatus RENAME TO tmp_registrationstatus')
    new_type.create(op.get_bind())
    op.execute('ALTER TABLE registrations ALTER COLUMN status TYPE registrationstatus USING status::text::registrationstatus')
    op.execute('ALTER TABLE registrations_history ALTER COLUMN status TYPE registrationstatus USING status::text::registrationstatus')
    op.execute('DROP TYPE tmp_registrationstatus')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute('ALTER TYPE registrationstatus RENAME TO tmp_registrationstatus')
    old_type.create(op.get_bind())
    op.execute('ALTER TABLE registrations ALTER COLUMN status TYPE registrationstatus USING status::text::registrationstatus')
    op.execute('ALTER TABLE registrations_history ALTER COLUMN status TYPE registrationstatus USING status::text::registrationstatus')
    op.execute('DROP TYPE tmp_registrationstatus')
    # ### end Alembic commands ###
