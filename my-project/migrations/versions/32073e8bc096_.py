"""empty message

Revision ID: 32073e8bc096
Revises: 295eb925d538
Create Date: 2023-04-20 08:29:33.723315

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '32073e8bc096'
down_revision = '295eb925d538'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('customers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=60), nullable=True),
    sa.Column('email_verified', sa.Boolean(), nullable=True),
    sa.Column('username', sa.String(length=60), nullable=True),
    sa.Column('first_name', sa.String(length=60), nullable=True),
    sa.Column('last_name', sa.String(length=60), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('customers', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_customers_email'), ['email'], unique=True)
        batch_op.create_index(batch_op.f('ix_customers_first_name'), ['first_name'], unique=False)
        batch_op.create_index(batch_op.f('ix_customers_last_name'), ['last_name'], unique=False)
        batch_op.create_index(batch_op.f('ix_customers_username'), ['username'], unique=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('customers', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_customers_username'))
        batch_op.drop_index(batch_op.f('ix_customers_last_name'))
        batch_op.drop_index(batch_op.f('ix_customers_first_name'))
        batch_op.drop_index(batch_op.f('ix_customers_email'))

    op.drop_table('customers')
    # ### end Alembic commands ###
