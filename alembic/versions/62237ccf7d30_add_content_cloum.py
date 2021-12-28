"""add content cloum

Revision ID: 62237ccf7d30
Revises: ad2230564ff0
Create Date: 2021-12-27 16:36:23.197200

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '62237ccf7d30'
down_revision = 'ad2230564ff0'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column ('content', sa.String(),nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
