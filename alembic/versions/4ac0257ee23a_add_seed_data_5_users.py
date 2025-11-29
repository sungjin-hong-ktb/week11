"""Add seed data - 5 users

Revision ID: 4ac0257ee23a
Revises: 3ac8ef21ba95
Create Date: 2025-11-29 14:44:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4ac0257ee23a'
down_revision: Union[str, Sequence[str], None] = '3ac8ef21ba95'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add 5 seed users."""
    # Create users table reference
    users_table = sa.table(
        'users',
        sa.column('email', sa.String),
        sa.column('nickname', sa.String),
        sa.column('hashed_password', sa.String)
    )

    # Insert 5 users
    op.bulk_insert(
        users_table,
        [
            {
                'email': 'hong@example.com',
                'nickname': '홍길동',
                'hashed_password': 'Password123!'
            },
            {
                'email': 'kim@example.com',
                'nickname': '김철수',
                'hashed_password': 'Password123!'
            },
            {
                'email': 'lee@example.com',
                'nickname': '이영희',
                'hashed_password': 'Password123!'
            },
            {
                'email': 'park@example.com',
                'nickname': '박민수',
                'hashed_password': 'Password123!'
            },
            {
                'email': 'choi@example.com',
                'nickname': '최지우',
                'hashed_password': 'Password123!'
            }
        ]
    )


def downgrade() -> None:
    """Remove seed users."""
    # Delete the 5 seed users
    op.execute(
        "DELETE FROM users WHERE email IN ("
        "'hong@example.com', 'kim@example.com', 'lee@example.com', "
        "'park@example.com', 'choi@example.com')"
    )
