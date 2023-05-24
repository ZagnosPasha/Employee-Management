"""empty message

Revision ID: 5af4174f7081
Revises: a97cdea0b55e
Create Date: 2023-04-13 11:59:25.984314

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5af4174f7081'
down_revision = 'a97cdea0b55e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('leaves',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('reason', sa.String(length=120), nullable=False),
    sa.Column('leave_date', sa.DateTime(), nullable=False),
    sa.Column('leave_duration', sa.Integer(), nullable=False),
    sa.Column('leave_assigned_to', sa.Integer(), nullable=True),
    sa.Column('approved', sa.Boolean(), nullable=True),
    sa.Column('submitted', sa.Boolean(), nullable=True),
    sa.Column('disproved', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['leave_assigned_to'], ['employees.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('employees', schema=None) as batch_op:
        batch_op.add_column(sa.Column('reamining_leave_days', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('employees', schema=None) as batch_op:
        batch_op.drop_column('reamining_leave_days')

    op.drop_table('leaves')
    # ### end Alembic commands ###