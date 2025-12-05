from sqlalchemy.orm import Session

from app.models.comment_model import Comment
from app.controllers.user_controller import UserController
from app.schemas.comment_schema import CommentCreate, CommentUpdate
from app.exceptions import NotFoundException, ForbiddenException
from app.utils.db_utils import db_transaction


class CommentController:
    def __init__(self, db: Session):
        self.db = db

    def create_comment(
        self,
        comment_data: CommentCreate,
        post_id: int,
        author_id: int
    ) -> Comment:
        """댓글 생성

        Args:
            comment_data (CommentCreate): 생성할 댓글 정보
            post_id (int): 게시글 ID
            author_id (int): 작성자 ID

        Returns:
            Comment: 생성된 댓글
        """
        # 작성자 존재 확인
        user = UserController(self.db).get_user_by_id(author_id)

        if not user:
            raise NotFoundException("작성자가 존재하지 않습니다")
        
        new_comment = Comment(
            content=comment_data.content,
            post_id=post_id,
            author_id=author_id
        )

        with db_transaction(self.db):
            self.db.add(new_comment)

        self.db.refresh(new_comment)
        return new_comment

    def get_comments_by_post(
        self,
        post_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> list[Comment]:
        """게시글의 모든 댓글 조회

        Args:
            post_id (int): 게시글 ID
            skip (int): 건너뛸 개수
            limit (int): 최대 개수

        Returns:
            list[Comment]: 댓글 리스트
        """
        return (
            self.db.query(Comment)
            .filter(Comment.post_id == post_id)
            .order_by(Comment.created_at.asc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_comment_by_id(self, comment_id: int) -> Comment | None:
        """ID로 댓글 조회

        Args:
            comment_id (int): 댓글 ID

        Returns:
            Comment | None: 댓글 정보 또는 None
        """
        return (
            self.db.query(Comment)
            .filter(Comment.id == comment_id)
            .first()
        )

    def update_comment(
        self,
        comment_id: int,
        comment_data: CommentUpdate,
        author_id: int
    ) -> Comment | None:
        """댓글 수정

        Args:
            comment_id (int): 댓글 ID
            comment_data (CommentUpdate): 수정할 댓글 정보
            author_id (int): 작성자 ID (권한 확인용)

        Returns:
            Comment | None: 수정된 댓글 또는 None

        Raises:
            ValueError: 작성자가 아닌 경우
        """
        # 댓글 존재 확인
        comment = self.get_comment_by_id(comment_id)
        if not comment:
            return None
        
        # 작성자 확인
        if comment.author_id != author_id:
            raise ForbiddenException("댓글 수정 권한이 없습니다")

        if comment_data.content:
            comment.content = comment_data.content

        with db_transaction(self.db):
            pass  # commit만 수행

        self.db.refresh(comment)
        return comment

    def delete_comment(
        self,
        comment_id: int,
        author_id: int
    ) -> Comment | None:
        """댓글 삭제

        Args:
            comment_id (int): 댓글 ID
            author_id (int): 작성자 ID (권한 확인용)

        Returns:
            Comment | None: 삭제된 댓글 또는 None

        Raises:
            ValueError: 작성자가 아닌 경우
        """
        # 댓글 존재 확인
        comment = self.get_comment_by_id(comment_id)
        if not comment:
            return None

        # 작성자 확인
        if comment.author_id != author_id:
            raise ForbiddenException("댓글 삭제 권한이 없습니다")

        with db_transaction(self.db):
            self.db.delete(comment)

        return comment