"""create posts table

Revision ID: 54e04a7416db
Revises: 
Create Date: 2022-03-20 02:39:57.305065

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '54e04a7416db'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True), 
    sa.Column('title', sa.String(), nullable=False))

def downgrade():
    op.drop_table('posts')
