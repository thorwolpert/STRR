"""empty message

Revision ID: bfdd00905978
Revises: d8b1f2dab56e
Create Date: 2024-07-31 07:16:52.379559

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'bfdd00905978'
down_revision = 'd8b1f2dab56e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('auto_approval_records', schema=None) as batch_op:
        batch_op.alter_column('application_id',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.drop_constraint('auto_approval_records_registration_id_fkey', type_='foreignkey')
        batch_op.drop_column('registration_id')

    with op.batch_alter_table('ltsa', schema=None) as batch_op:
        batch_op.alter_column('application_id',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.drop_constraint('ltsa_registration_id_fkey', type_='foreignkey')
        batch_op.drop_column('registration_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('ltsa', schema=None) as batch_op:
        batch_op.add_column(sa.Column('registration_id', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.create_foreign_key('ltsa_registration_id_fkey', 'registrations', ['registration_id'], ['id'])
        batch_op.alter_column('application_id',
               existing_type=sa.INTEGER(),
               nullable=True)

    with op.batch_alter_table('auto_approval_records', schema=None) as batch_op:
        batch_op.add_column(sa.Column('registration_id', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.create_foreign_key('auto_approval_records_registration_id_fkey', 'registrations', ['registration_id'], ['id'])
        batch_op.alter_column('application_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###