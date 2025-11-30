"""Add seed data for posts and comments

Revision ID: f2e035a78b12
Revises: e1d015e51a39
Create Date: 2025-11-29 22:00:00.000000

"""
from typing import Sequence, Union
from datetime import datetime

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f2e035a78b12'
down_revision: Union[str, Sequence[str], None] = 'e1d015e51a39'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add seed posts and comments."""
    # Create posts table reference
    posts_table = sa.table(
        'posts',
        sa.column('title', sa.String),
        sa.column('content', sa.Text),
        sa.column('image_url', sa.String),
        sa.column('created_at', sa.DateTime),
        sa.column('view_count', sa.Integer),
        sa.column('like_count', sa.Integer),
        sa.column('author_id', sa.Integer)
    )

    # Create comments table reference
    comments_table = sa.table(
        'comments',
        sa.column('content', sa.Text),
        sa.column('created_at', sa.DateTime),
        sa.column('post_id', sa.Integer),
        sa.column('author_id', sa.Integer)
    )

    # Insert 10 posts
    op.bulk_insert(
        posts_table,
        [
            {
                'title': 'FastAPI 시작하기',
                'content': 'FastAPI는 현대적이고 빠른 웹 프레임워크입니다. Python 3.7+ 기반으로 표준 Python 타입 힌트를 사용하여 API를 구축할 수 있습니다.',
                'image_url': '/images/fastapi_intro.jpg',
                'created_at': datetime(2025, 11, 1, 10, 0, 0),
                'view_count': 125,
                'like_count': 23,
                'author_id': 1
            },
            {
                'title': 'SQLAlchemy ORM 완벽 가이드',
                'content': 'SQLAlchemy는 Python에서 가장 인기있는 ORM입니다. 데이터베이스 작업을 객체 지향적으로 처리할 수 있습니다.',
                'image_url': None,
                'created_at': datetime(2025, 11, 5, 14, 30, 0),
                'view_count': 89,
                'like_count': 15,
                'author_id': 2
            },
            {
                'title': 'Pydantic으로 데이터 검증하기',
                'content': 'Pydantic은 Python 타입 힌트를 사용한 데이터 검증 라이브러리입니다. FastAPI와 완벽하게 통합됩니다.',
                'image_url': '/images/pydantic.jpg',
                'created_at': datetime(2025, 11, 10, 9, 15, 0),
                'view_count': 67,
                'like_count': 12,
                'author_id': 3
            },
            {
                'title': 'RESTful API 디자인 베스트 프랙티스',
                'content': 'REST API를 설계할 때 지켜야 할 원칙들과 HTTP 메서드, 상태 코드 사용법에 대해 알아봅니다.',
                'image_url': None,
                'created_at': datetime(2025, 11, 12, 16, 45, 0),
                'view_count': 156,
                'like_count': 34,
                'author_id': 1
            },
            {
                'title': 'Alembic으로 데이터베이스 마이그레이션',
                'content': 'Alembic은 SQLAlchemy를 위한 데이터베이스 마이그레이션 도구입니다. 스키마 변경 이력을 관리할 수 있습니다.',
                'image_url': '/images/alembic.jpg',
                'created_at': datetime(2025, 11, 15, 11, 20, 0),
                'view_count': 43,
                'like_count': 8,
                'author_id': 4
            },
            {
                'title': 'Python 비동기 프로그래밍 (async/await)',
                'content': 'Python의 asyncio를 사용한 비동기 프로그래밍에 대해 배워봅니다. FastAPI에서 async 함수를 활용하는 방법도 다룹니다.',
                'image_url': None,
                'created_at': datetime(2025, 11, 18, 13, 10, 0),
                'view_count': 201,
                'like_count': 45,
                'author_id': 5
            },
            {
                'title': 'JWT 인증 구현하기',
                'content': 'FastAPI에서 JWT 토큰 기반 인증을 구현하는 방법을 단계별로 설명합니다.',
                'image_url': '/images/jwt_auth.jpg',
                'created_at': datetime(2025, 11, 20, 15, 30, 0),
                'view_count': 178,
                'like_count': 39,
                'author_id': 2
            },
            {
                'title': 'Docker로 FastAPI 배포하기',
                'content': 'Dockerfile을 작성하고 FastAPI 애플리케이션을 컨테이너화하여 배포하는 방법을 알아봅니다.',
                'image_url': None,
                'created_at': datetime(2025, 11, 22, 10, 0, 0),
                'view_count': 92,
                'like_count': 18,
                'author_id': 3
            },
            {
                'title': 'FastAPI 테스트 작성하기',
                'content': 'pytest와 TestClient를 사용하여 FastAPI 엔드포인트를 테스트하는 방법을 배워봅니다.',
                'image_url': '/images/testing.jpg',
                'created_at': datetime(2025, 11, 25, 14, 45, 0),
                'view_count': 54,
                'like_count': 11,
                'author_id': 1
            },
            {
                'title': 'CORS 설정 완벽 가이드',
                'content': 'FastAPI에서 CORS를 올바르게 설정하여 프론트엔드와 안전하게 통신하는 방법을 설명합니다.',
                'image_url': None,
                'created_at': datetime(2025, 11, 28, 9, 30, 0),
                'view_count': 36,
                'like_count': 7,
                'author_id': 4
            }
        ]
    )

    # Insert 25 comments (multiple comments per post)
    op.bulk_insert(
        comments_table,
        [
            # Comments for Post 1
            {
                'content': '정말 유익한 글이네요! FastAPI 입문하는데 큰 도움이 되었습니다.',
                'created_at': datetime(2025, 11, 1, 12, 30, 0),
                'post_id': 1,
                'author_id': 2
            },
            {
                'content': 'FastAPI의 자동 문서화 기능이 정말 편리하더라구요.',
                'created_at': datetime(2025, 11, 2, 8, 15, 0),
                'post_id': 1,
                'author_id': 3
            },
            {
                'content': '다음 포스트도 기대하겠습니다!',
                'created_at': datetime(2025, 11, 3, 16, 20, 0),
                'post_id': 1,
                'author_id': 5
            },
            # Comments for Post 2
            {
                'content': 'SQLAlchemy 관계 설정 부분이 어려웠는데 이해가 됐어요.',
                'created_at': datetime(2025, 11, 6, 10, 45, 0),
                'post_id': 2,
                'author_id': 1
            },
            {
                'content': 'ORM을 사용하면 SQL을 몰라도 되나요?',
                'created_at': datetime(2025, 11, 7, 14, 0, 0),
                'post_id': 2,
                'author_id': 4
            },
            # Comments for Post 3
            {
                'content': 'Pydantic validator 사용 예제가 도움이 됐습니다.',
                'created_at': datetime(2025, 11, 11, 9, 30, 0),
                'post_id': 3,
                'author_id': 2
            },
            {
                'content': '복잡한 데이터 구조도 검증 가능한가요?',
                'created_at': datetime(2025, 11, 12, 11, 15, 0),
                'post_id': 3,
                'author_id': 5
            },
            {
                'content': 'Field 설정 옵션들이 다양하네요. 감사합니다!',
                'created_at': datetime(2025, 11, 13, 15, 40, 0),
                'post_id': 3,
                'author_id': 1
            },
            # Comments for Post 4
            {
                'content': 'RESTful API 원칙을 명확하게 설명해주셨네요.',
                'created_at': datetime(2025, 11, 13, 10, 20, 0),
                'post_id': 4,
                'author_id': 3
            },
            {
                'content': 'PUT vs PATCH 차이를 드디어 이해했습니다!',
                'created_at': datetime(2025, 11, 14, 13, 50, 0),
                'post_id': 4,
                'author_id': 4
            },
            # Comments for Post 5
            {
                'content': 'Alembic 명령어 정리가 잘 되어있네요.',
                'created_at': datetime(2025, 11, 16, 9, 0, 0),
                'post_id': 5,
                'author_id': 1
            },
            {
                'content': '마이그레이션 롤백은 어떻게 하나요?',
                'created_at': datetime(2025, 11, 17, 14, 30, 0),
                'post_id': 5,
                'author_id': 2
            },
            {
                'content': 'downgrade 함수를 작성하면 됩니다!',
                'created_at': datetime(2025, 11, 17, 15, 10, 0),
                'post_id': 5,
                'author_id': 4
            },
            # Comments for Post 6
            {
                'content': 'async/await 개념이 이제 확실히 잡혔어요.',
                'created_at': datetime(2025, 11, 19, 10, 15, 0),
                'post_id': 6,
                'author_id': 3
            },
            {
                'content': '비동기 DB 작업도 다뤄주시면 좋겠습니다.',
                'created_at': datetime(2025, 11, 20, 11, 40, 0),
                'post_id': 6,
                'author_id': 1
            },
            {
                'content': 'asyncio.gather() 사용법도 궁금합니다!',
                'created_at': datetime(2025, 11, 21, 16, 20, 0),
                'post_id': 6,
                'author_id': 5
            },
            # Comments for Post 7
            {
                'content': 'JWT 구현 예제 코드가 정말 도움됐습니다.',
                'created_at': datetime(2025, 11, 21, 9, 30, 0),
                'post_id': 7,
                'author_id': 4
            },
            {
                'content': 'refresh token도 함께 구현하는게 좋을까요?',
                'created_at': datetime(2025, 11, 22, 13, 0, 0),
                'post_id': 7,
                'author_id': 5
            },
            {
                'content': '보안을 위해서는 refresh token이 필수입니다!',
                'created_at': datetime(2025, 11, 22, 14, 15, 0),
                'post_id': 7,
                'author_id': 2
            },
            # Comments for Post 8
            {
                'content': 'Docker 이미지 크기를 줄이는 팁도 알려주세요.',
                'created_at': datetime(2025, 11, 23, 10, 45, 0),
                'post_id': 8,
                'author_id': 1
            },
            {
                'content': 'multi-stage build를 사용하면 됩니다!',
                'created_at': datetime(2025, 11, 23, 11, 30, 0),
                'post_id': 8,
                'author_id': 3
            },
            # Comments for Post 9
            {
                'content': 'pytest fixture 활용법이 인상적이네요.',
                'created_at': datetime(2025, 11, 26, 9, 20, 0),
                'post_id': 9,
                'author_id': 2
            },
            {
                'content': '테스트 커버리지는 어느정도가 적당할까요?',
                'created_at': datetime(2025, 11, 27, 15, 0, 0),
                'post_id': 9,
                'author_id': 4
            },
            # Comments for Post 10
            {
                'content': 'CORS 에러 해결에 큰 도움이 되었습니다!',
                'created_at': datetime(2025, 11, 28, 11, 0, 0),
                'post_id': 10,
                'author_id': 3
            },
            {
                'content': '프로덕션 환경에서 주의할 점도 알려주세요.',
                'created_at': datetime(2025, 11, 29, 10, 30, 0),
                'post_id': 10,
                'author_id': 5
            }
        ]
    )


def downgrade() -> None:
    """Remove seed posts and comments."""
    # Delete comments first (due to foreign key constraint)
    op.execute("DELETE FROM comments WHERE post_id BETWEEN 1 AND 10")

    # Delete posts
    op.execute("DELETE FROM posts WHERE id BETWEEN 1 AND 10")
