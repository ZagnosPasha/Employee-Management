"""empty message

Revision ID: f3d2f73e5811
Revises: 0abf893ec21e
Create Date: 2023-04-16 12:16:03.938006

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f3d2f73e5811'
down_revision = '0abf893ec21e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('packages', schema=None) as batch_op:
        batch_op.create_unique_constraint(None, ['name'])

    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.create_unique_constraint(None, ['name'])

    with op.batch_alter_table('teas', schema=None) as batch_op:
        batch_op.create_unique_constraint(None, ['name'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('teas', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')

    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')

    with op.batch_alter_table('packages', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')

    # ### end Alembic commands ###
