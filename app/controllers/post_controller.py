from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from app.models.post_model import Post
from app.controllers.user_controller import UserController
from app.schemas.post_schema import PostCreate, PostUpdate
from app.schemas.user_schema import User


class PostController:
    """게시글 관련 비즈니스 로직을 처리하는 컨트롤러"""

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
        user = UserController(self.db).get_user_by_id(author_id)
        if not user:
            raise ValueError("작성자가 존재하지 않습니다")

        new_post = Post(
            title=post_data.title,
            content=post_data.content,
            image_url=post_data.image_url,
            author_id=author_id
        )
        try:
            self.db.add(new_post)
            self.db.commit()
            self.db.refresh(new_post)
        except IntegrityError:
            self.db.rollback()
            raise ValueError("유효하지 않은 데이터입니다")
        except SQLAlchemyError:
            self.db.rollback()
            raise RuntimeError("데이터베이스 오류가 발생했습니다")
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
        return (
            self.db.query(Post)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_post_by_id(self, post_id: int) -> Post | None:
        """ID로 게시글 조회 (조회수 증가)

        Args:
            post_id (int): 게시글 ID

        Returns:
            Post | None: 게시글 정보 또는 None
        """
        post = (
            self.db.query(Post)
            .filter(Post.id == post_id)
            .first()
        )
        if post:
            post.view_count += 1
            try:
                self.db.commit()
                self.db.refresh(post)
            except SQLAlchemyError:
                self.db.rollback()
                raise RuntimeError("데이터베이스 오류가 발생했습니다")
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
        post = (
            self.db.query(Post)
            .filter(Post.id == post_id)
            .first()
        )
        if not post:
            return None

        # 작성자 확인
        if post.author_id != author_id:
            raise ValueError("게시글 수정 권한이 없습니다")

        # 수정
        if post_data.title:
            post.title = post_data.title
        if post_data.content:
            post.content = post_data.content
        if post_data.image_url is not None:
            post.image_url = post_data.image_url

        try:
            self.db.commit()
            self.db.refresh(post)
        except IntegrityError:
            self.db.rollback()
            raise ValueError("유효하지 않은 데이터입니다")
        except SQLAlchemyError:
            self.db.rollback()
            raise RuntimeError("데이터베이스 오류가 발생했습니다")
        
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
        post = (
            self.db.query(Post)
            .filter(Post.id == post_id)
            .first()
        )
        if not post:
            return None

        # 작성자 확인
        if post.author_id != author_id:
            raise ValueError("게시글 삭제 권한이 없습니다")
        try:
            self.db.delete(post)
            self.db.commit()
        except IntegrityError:
            self.db.rollback()
            raise ValueError("유효하지 않은 데이터입니다")
        except SQLAlchemyError:
            self.db.rollback()
            raise RuntimeError("데이터베이스 오류가 발생했습니다")

        return post
