"""add foreign ke to post table

Revision ID: 08cfa035b520
Revises: 4817c8af6189
Create Date: 2021-12-27 16:53:46.645050

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '08cfa035b520'
down_revision = '4817c8af6189'
branch_labels = None
depends_on = None


def upgrade():

    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fk', source_table="posts", referent_table='users', local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")

    pass


def downgrade():
    op.drop_constraint("post_user_fk", table_name="posts")
    op.drop_column('posts', 'owner_id')
    pass
