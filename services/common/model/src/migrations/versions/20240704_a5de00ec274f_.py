"""empty message

Revision ID: a5de00ec274f
Revises: 420791ae10dc
Create Date: 2024-07-04 21:42:05.605033

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'a5de00ec274f'
down_revision = '420791ae10dc'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('contacts', schema=None) as batch_op:
        batch_op.add_column(sa.Column('social_insurance_number', sa.VARCHAR(), nullable=True))
        batch_op.add_column(sa.Column('business_number', sa.VARCHAR(), nullable=True))


def downgrade():
    with op.batch_alter_table('contacts', schema=None) as batch_op:
        batch_op.drop_column('social_insurance_number')
        batch_op.drop_column('business_number')
