"""add content column to posts table

Revision ID: 439e5f1e5017
Revises: 54e04a7416db
Create Date: 2022-04-18 02:29:27.344056

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '439e5f1e5017'
down_revision = '54e04a7416db'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))


def downgrade():
    op.drop_column('posts','content')
