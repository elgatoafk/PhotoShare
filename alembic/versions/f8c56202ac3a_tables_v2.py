"""Tables v2

Revision ID: f8c56202ac3a
Revises: d52b8f2ff0e9
Create Date: 2024-07-29 16:57:17.675727

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'f8c56202ac3a'
down_revision: Union[str, None] = 'd52b8f2ff0e9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    # ### end Alembic commands ###
    
    op.create_table('users',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('users_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('username', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('email', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('full_name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('hashed_password', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('disabled', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('role', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('registered_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('is_active', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='users_pkey'),
    sa.UniqueConstraint('email', name='users_email_key'),
    sa.UniqueConstraint('username', name='users_username_key'),
    postgresql_ignore_search_path=False
    )
    op.create_table('photos',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('photos_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('description', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('url', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='photos_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='photos_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('tags',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('tag_name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='tags_pkey'),
    sa.UniqueConstraint('tag_name', name='tags_tag_name_key')
    )
    op.create_table('ratings',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('rating', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('photo_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['photo_id'], ['photos.id'], name='ratings_photo_id_fkey'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='ratings_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='ratings_pkey')
    )
    op.create_index('ix_ratings_rating', 'ratings', ['rating'], unique=False)
    op.create_table('tokens',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('token', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('expires_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='tokens_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='tokens_pkey'),
    sa.UniqueConstraint('token', name='tokens_token_key')
    )
    op.create_table('photo_m2m_tag',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('photo_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('tag_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['photo_id'], ['photos.id'], name='photo_m2m_tag_photo_id_fkey', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['tag_id'], ['tags.id'], name='photo_m2m_tag_tag_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name='photo_m2m_tag_pkey')
    )
    
    
    op.create_table('blacklisted_tokens',
    sa.Column('token', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('blacklisted_on', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('token', name='blacklisted_tokens_pkey')
    )
    op.create_table('comments',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('content', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('photo_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('updated_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['photo_id'], ['photos.id'], name='comments_photo_id_fkey'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='comments_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='comments_pkey')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
