"""add_influence_score_to_articles

Revision ID: c7d8e9f1a2b3
Revises: b6a562171675
Create Date: 2025-12-31 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c7d8e9f1a2b3'
down_revision = 'b6a562171675'
branch_labels = None
depends_on = None


def upgrade():
    # Add influence_score column
    op.add_column('articles', sa.Column('influence_score', sa.Float(), nullable=True))

    # Set default value for existing records
    op.execute('UPDATE articles SET influence_score = 0.0 WHERE influence_score IS NULL')

    # Make column non-nullable after setting defaults
    op.alter_column('articles', 'influence_score',
               existing_type=sa.Float(),
               nullable=False,
               server_default='0.0')

    # Create index
    op.create_index('ix_articles_influence', 'articles', ['influence_score'], unique=False)


def downgrade():
    op.drop_index('ix_articles_influence', table_name='articles')
    op.drop_column('articles', 'influence_score')
