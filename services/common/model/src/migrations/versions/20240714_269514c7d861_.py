"""empty message

Revision ID: 269514c7d861
Revises: ed33e07431ea
Create Date: 2024-07-14 22:20:59.662520

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '269514c7d861'
down_revision = 'ed33e07431ea'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('certificates',
                    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
                    sa.Column('registration_id', sa.INTEGER(), nullable=False),
                    sa.Column('registration_number', sa.VARCHAR(), nullable=False, unique=True),
                    sa.Column('creation_date', postgresql.TIMESTAMP(
                    ), nullable=False, server_default=sa.text('(NOW())')),
                    sa.Column('expiry_date', postgresql.TIMESTAMP(
                    ), nullable=False, server_default=sa.text("(NOW() + interval '1 year')")),
                    sa.Column('certificate', postgresql.BYTEA(), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.ForeignKeyConstraint(['registration_id'], [
                        'registrations.id'], name='certificates_registration_id_fkey')
                    )


def downgrade():
    op.drop_table('certificates')
