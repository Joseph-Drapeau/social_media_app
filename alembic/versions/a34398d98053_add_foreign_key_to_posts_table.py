"""add foreign-key to posts table

Revision ID: a34398d98053
Revises: 8168309d7792
Create Date: 2022-04-18 02:43:21.796789

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a34398d98053'
down_revision = '8168309d7792'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'posts', 
        sa.Column('owner_id', sa.Integer(), nullable=False)
    )

    op.create_foreign_key(
        'posts_users_fk', 
        source_table='posts', 
        referent_table='users',
        local_cols=['owner_id'], 
        remote_cols=['id'], 
        ondelete='CASCADE'
    )


def downgrade():
    op.drop_constraint(
        'post_users_fk', 
        table_name='posts'
    )

    op.drop_column(
        'posts',
        'owner_id'
    )