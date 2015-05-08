"""User registered at.

Revision ID: 48a2c95c625
Revises: 54792542f32
Create Date: 2015-05-08 13:23:27.933346

"""

# revision identifiers, used by Alembic.
revision = '48a2c95c625'
down_revision = '54792542f32'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('auth_users', sa.Column('registered_at', sa.DateTime(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('auth_users', 'registered_at')
    ### end Alembic commands ###
