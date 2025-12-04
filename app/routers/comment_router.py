from fastapi import APIRouter, Depends, HTTPException, status, Query, Path, Body, Header
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.comment_schema import Comment, CommentUpdate
from app.controllers.comment_controller import CommentController

router = APIRouter(
    prefix="/comments",
    tags=["comments"]
)

@router.get(
    "/{comment_id}",
    response_model=Comment,
    description="특정 댓글 조회"
)
def get_comment(
    comment_id: int = Path(..., description="조회할 댓글 ID"),
    db: Session = Depends(get_db)
):
    """댓글 조회

    Args:
        comment_id (int): 댓글 ID
        db (Session): 데이터베이스 세션

    Returns:
        Comment: 댓글 정보

    Raises:
        HTTPException: 댓글이 존재하지 않을 경우
    """
    controller = CommentController(db)
    comment = controller.get_comment_by_id(comment_id)
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="댓글을 찾을 수 없습니다"
        )
    return comment


@router.put(
    "/{comment_id}",
    response_model=Comment,
    description="댓글 수정 (작성자만 가능)"
)
def update_comment(
    comment_id: int = Path(..., description="수정할 댓글 ID"),
    comment_data: CommentUpdate = Body(...),
    db: Session = Depends(get_db)
):
    """댓글 수정

    Args:
        comment_id (int): 댓글 ID
        comment_data (CommentUpdate): 수정할 댓글 정보 (author_id 포함)
        db (Session): 데이터베이스 세션

    Returns:
        Comment: 수정된 댓글

    Raises:
        HTTPException: 댓글이 존재하지 않거나 권한이 없을 경우
    """
    try:
        controller = CommentController(db)
        comment = controller.update_comment(
            comment_id,
            comment_data,
            comment_data.author_id
        )
        if not comment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="댓글을 찾을 수 없습니다"
            )
        return comment
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )


@router.delete(
    "/{comment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="댓글 삭제 (작성자만 가능)"
)
def delete_comment(
    comment_id: int = Path(..., description="삭제할 댓글 ID"),
    x_user_id: int = Header(
        ...,
        alias="X-User-ID",
        description="작성자 ID (권한 확인용)"
    ),
    db: Session = Depends(get_db)
):
    """댓글 삭제

    Args:
        comment_id (int): 댓글 ID
        x_user_id (int): 헤더로 전달된 작성자 ID (권한 확인용)
        db (Session): 데이터베이스 세션

    Raises:
        HTTPException: 댓글이 존재하지 않거나 권한이 없을 경우
    """
    try:
        controller = CommentController(db)
        comment = controller.delete_comment(comment_id, x_user_id)
        if not comment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="댓글을 찾을 수 없습니다"
            )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )
