""" Add interactions model
Revision ID: f25ac17d6c02
Revises: a43ed28f2c01
Create Date: 2026-03-11 23:01:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'f25ac17d6c02'
down_revision = 'a43ed28f2c01'
branch_labels = None 
depends_on = None


def upgrade() -> None:

    with op.get_context().autocommit_block():
        op.execute("ALTER TYPE interactionstatus ADD VALUE 'QUEUED' BEFORE 'SENT'")

    channel_enum = postgresql.ENUM('EMAIL', 'SMS', 'PHONE', 'SYSTEM', name='channeltype', create_type=False)

    status_enum = postgresql.ENUM('QUEUED', 'SENT', 'DELIVERED', 'FAILED', 'OPENED', name='interactionstatus', create_type=False)

    with op.batch_alter_table('interactions', schema=None) as batch_op:
        batch_op.add_column(sa.Column('version', sa.Integer(), nullable=False))
        batch_op.alter_column('idempotency_key', 
               existing_type=sa.VARCHAR(),
               nullable=True)
    
    op.drop_index(op.f('ix_interactions_idempotency_key'), table_name='interactions')
    op.create_index(
        op.f('ix_interactions_idempotency_key'), 
        'interactions', 
        ['idempotency_key'], 
        unique=False
    )

    op.create_table(
        'interactions_history',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('interaction_uuid', sa.String(length=36), nullable=False),
        sa.Column('idempotency_key', sa.String(length=255), nullable=True),
        
        # Enum Columns
        sa.Column('channel', channel_enum, nullable=False),
        sa.Column('status', status_enum, nullable=False),
        
        sa.Column('body_content', sa.Text(), nullable=True),
        sa.Column('notify_reference', sa.String(length=100), nullable=True),
        sa.Column('provider_reference', sa.String(length=100), nullable=True),
        sa.Column('meta_data', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        
        # Foreign Key Columns
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('customer_id', sa.Integer(), nullable=True),
        sa.Column('application_id', sa.Integer(), nullable=True),
        sa.Column('registration_id', sa.Integer(), nullable=True),
        
        # Version
        sa.Column('version', sa.Integer(), autoincrement=False, nullable=False),
        sa.Column('changed', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id', 'version'),# Primary Key
        
        # Foreign Key Constraints
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['customer_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['application_id'], ['application.id'], ),
        sa.ForeignKeyConstraint(['registration_id'], ['registrations.id'], ),
    )

    # 3. Create Indexes and Unique Constraints
    op.create_index(op.f('ix_interactions_hist_interaction_uuid'), 'interactions', ['interaction_uuid'], unique=False)
    op.create_index(op.f('ix_interactions_hist_idempotency_key'), 'interactions', ['idempotency_key'], unique=False)
    
    op.create_index(op.f('ix_interactions_hist_notify_reference'), 'interactions', ['notify_reference'], unique=False)
    op.create_index(op.f('ix_interactions_hist_provider_reference'), 'interactions', ['provider_reference'], unique=False)
    
    op.create_index(op.f('ix_interactions_hist_customer_id'), 'interactions', ['customer_id'], unique=False)
    op.create_index(op.f('ix_interactions_hist_user_id'), 'interactions', ['user_id'], unique=False)
    op.create_index(op.f('ix_interactions_hist_application_id'), 'interactions', ['application_id'], unique=False)
    op.create_index(op.f('ix_interactions_hist_registration_id'), 'interactions', ['registration_id'], unique=False)


def downgrade() -> None:
    op.execute("ALTER TYPE interactionstatus RENAME TO interactionstatus_old")
    op.execute("CREATE TYPE interactionstatus AS ENUM ('SENT', 'DELIVERED', 'FAILED', 'OPENED')")

    op.execute(
        "ALTER TABLE interactions ALTER COLUMN status TYPE interactionstatus "
        "USING status::text::interactionstatus"
    )

    op.execute("DROP TYPE interactionstatus_old")
    op.drop_table('interactions_history')
