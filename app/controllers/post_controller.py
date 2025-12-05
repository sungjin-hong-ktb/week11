from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.post_model import Post
from app.models.comment_model import Comment
from app.controllers.user_controller import UserController
from app.schemas.post_schema import PostCreate, PostUpdate
from app.exceptions import NotFoundException, ForbiddenException
from app.utils.db_utils import db_transaction


class PostController:
    def __init__(self, db: Session):
        self.db = db

    def create_post(
        self,
        post_data: PostCreate,
        author_id: int
    ) -> Post:
        """게시글 생성

        Args:
            post_data (PostCreate): 생성할 게시글 정보
            author_id (int): 작성자 ID

        Returns:
            Post: 생성된 게시글
        """
        # 작성자 존재 확인
        user = UserController(self.db).get_user_by_id(author_id)
        if not user:
            raise NotFoundException("작성자가 존재하지 않습니다")

        new_post = Post(
            title=post_data.title,
            content=post_data.content,
            image_url=post_data.image_url,
            author_id=author_id
        )

        with db_transaction(self.db):
            self.db.add(new_post)

        self.db.refresh(new_post)
        return new_post

    def get_posts(
        self,
        skip: int = 0,
        limit: int = 100
    ) -> list[Post]:
        """모든 게시글 조회

        Args:
            skip (int): 건너뛸 개수
            limit (int): 최대 개수

        Returns:
            list[Post]: 게시글 리스트
        """
        # 게시글과 댓글 개수 조회
        results = (
            self.db.query(
                Post,
                func.count(Comment.id).label('comment_count')
            )
            .outerjoin(Comment, Post.id == Comment.post_id)
            .group_by(Post.id)
            .order_by(Post.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

        # Post 객체에 comment_count 추가
        posts = []
        for post, count in results:
            post.comment_count = count
            posts.append(post)

        return posts

    def get_post_by_id(self, post_id: int, increment_view: bool = True) -> Post | None:
        """ID로 게시글 조회 (조회수 증가)

        Args:
            post_id (int): 게시글 ID
            increment_view (bool): 조회수 증가 여부 (기본값: True)

        Returns:
            Post | None: 게시글 정보 또는 None
        """
        post = (
            self.db.query(Post)
            .filter(Post.id == post_id)
            .first()
        )
        if post and increment_view:
            post.view_count += 1
            with db_transaction(self.db):
                pass
            self.db.refresh(post)

        return post

    def update_post(
        self,
        post_id: int,
        post_data: PostUpdate,
        author_id: int
    ) -> Post | None:
        """게시글 수정

        Args:
            post_id (int): 게시글 ID
            post_data (PostUpdate): 수정할 게시글 정보
            author_id (int): 작성자 ID (권한 확인용)

        Returns:
            Post | None: 수정된 게시글 또는 None

        Raises:
            ValueError: 작성자가 아닌 경우
        """
        post = self.get_post_by_id(post_id, increment_view=False)
        if not post:
            return None

        # 작성자 확인
        if post.author_id != author_id:
            raise ForbiddenException("게시글 수정 권한이 없습니다")

        # 수정
        if post_data.title:
            post.title = post_data.title
        if post_data.content:
            post.content = post_data.content
        if post_data.image_url is not None:
            post.image_url = post_data.image_url

        with db_transaction(self.db):
            pass

        self.db.refresh(post)
        return post

    def delete_post(
        self,
        post_id: int,
        author_id: int
    ) -> Post | None:
        """게시글 삭제

        Args:
            post_id (int): 게시글 ID
            author_id (int): 작성자 ID (권한 확인용)

        Returns:
            Post | None: 삭제된 게시글 또는 None

        Raises:
            ValueError: 작성자가 아닌 경우
        """
        post = self.get_post_by_id(post_id, increment_view=False)
        if not post:
            return None

        # 작성자 확인
        if post.author_id != author_id:
            raise ForbiddenException("게시글 삭제 권한이 없습니다")

        with db_transaction(self.db):
            self.db.delete(post)

        return post