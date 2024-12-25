"""empty message

Revision ID: aa4d983f79c4
Revises: 412aa6608c42
Create Date: 2024-07-03 14:24:54.566539

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'aa4d983f79c4'
down_revision = '412aa6608c42'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('ltsa',
                    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
                    sa.Column('registration_id', sa.INTEGER(), nullable=False),
                    sa.Column('record', postgresql.JSONB(), nullable=False),
                    sa.Column('creation_date', postgresql.TIMESTAMP(
                    ), nullable=False, server_default=sa.text('(NOW())')),
                    sa.PrimaryKeyConstraint('id'),
                    sa.ForeignKeyConstraint(['registration_id'], [
                        'registrations.id'], name='ltsa_registration_id_fkey')
                    )

    op.create_table('auto_approval_records',
                    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
                    sa.Column('registration_id', sa.INTEGER(), nullable=False),
                    sa.Column('record', postgresql.JSONB(), nullable=False),
                    sa.Column('creation_date', postgresql.TIMESTAMP(
                    ), nullable=False, server_default=sa.text('(NOW())')),
                    sa.PrimaryKeyConstraint('id'),
                    sa.ForeignKeyConstraint(['registration_id'], [
                        'registrations.id'], name='auto_approval_records_registration_id_fkey')
                    )


def downgrade():
    op.drop_table('ltsa')
    op.drop_table('auto_approval_records')
