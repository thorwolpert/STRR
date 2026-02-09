""" Add interactions model
Revision ID: a43ed28f2c01
Revises: e50cd13c4d12
Create Date: 2026-02-06 12:01:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'a43ed28f2c01'
down_revision = 'e50cd13c4d12'
branch_labels = None 
depends_on = None


def upgrade() -> None:
    channel_enum = postgresql.ENUM('EMAIL', 'SMS', 'PHONE', 'SYSTEM', name='channeltype', create_type=False)
    channel_enum.create(op.get_bind(), checkfirst=True)

    status_enum = postgresql.ENUM('SENT', 'DELIVERED', 'FAILED', 'OPENED', name='interactionstatus', create_type=False)
    status_enum.create(op.get_bind(), checkfirst=True)

    # 2. Create the Table
    op.create_table(
        'interactions',
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
        
        # Primary Key
        sa.PrimaryKeyConstraint('id'),
        
        # Foreign Key Constraints
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['customer_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['application_id'], ['application.id'], ),
        sa.ForeignKeyConstraint(['registration_id'], ['registrations.id'], ),
        
        # Exclusive Check Constraint
        sa.CheckConstraint(
            'num_nonnulls(customer_id, application_id, registration_id) = 1',
            name='check_exclusive_owner_interaction'
        )
    )

    # 3. Create Indexes and Unique Constraints
    op.create_index(op.f('ix_interactions_interaction_uuid'), 'interactions', ['interaction_uuid'], unique=True)
    op.create_index(op.f('ix_interactions_idempotency_key'), 'interactions', ['idempotency_key'], unique=True)
    
    op.create_index(op.f('ix_interactions_notify_reference'), 'interactions', ['notify_reference'], unique=False)
    op.create_index(op.f('ix_interactions_provider_reference'), 'interactions', ['provider_reference'], unique=False)
    
    op.create_index(op.f('ix_interactions_customer_id'), 'interactions', ['customer_id'], unique=False)
    op.create_index(op.f('ix_interactions_user_id'), 'interactions', ['user_id'], unique=False)
    op.create_index(op.f('ix_interactions_application_id'), 'interactions', ['application_id'], unique=False)
    op.create_index(op.f('ix_interactions_registration_id'), 'interactions', ['registration_id'], unique=False)


def downgrade() -> None:
    op.drop_table('interactions')

    sa.Enum(name='interactionstatus').drop(op.get_bind(), checkfirst=True)
    sa.Enum(name='channeltype').drop(op.get_bind(), checkfirst=True)