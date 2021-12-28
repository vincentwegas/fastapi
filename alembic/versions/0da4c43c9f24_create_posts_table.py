"""create posts table

Revision ID: 0da4c43c9f24
Revises: 
Create Date: 2021-12-27 16:14:55.352670

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0da4c43c9f24'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("posts", sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
    sa.Column("title", sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_table('posts')
    pass
