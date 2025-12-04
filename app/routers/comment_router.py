from fastapi import APIRouter, Depends, HTTPException, status, Query, Path, Body
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.comment_schema import Comment, CommentCreate, CommentUpdate
from app.controllers.comment_controller import CommentController

router = APIRouter(
    prefix="/comments",
    tags=["comments"]
)


@router.post("/", response_model=Comment, status_code=status.HTTP_201_CREATED, description="새로운 댓글 작성")
def create_comment(
    comment_data: CommentCreate,
    post_id: int = Query(..., description="게시글 ID"),
    author_id: int = Query(..., description="작성자 ID"),
    db: Session = Depends(get_db)
):
    """댓글 생성

    Args:
        comment_data (CommentCreate): 생성할 댓글 정보
        post_id (int): 게시글 ID
        author_id (int): 작성자 ID
        db (Session): 데이터베이스 세션

    Returns:
        Comment: 생성된 댓글
    """
    controller = CommentController(db)
    return controller.create_comment(comment_data, post_id, author_id)


@router.get("/", response_model=list[Comment], description="특정 게시글의 댓글 목록 조회")
def get_comments(
    post_id: int = Query(..., description="게시글 ID"),
    skip: int = Query(0, ge=0, description="건너뛸 개수"),
    limit: int = Query(10, ge=1, le=100, description="최대 조회 개수"),
    db: Session = Depends(get_db)
):
    """게시글의 모든 댓글 조회

    Args:
        post_id (int): 게시글 ID
        skip (int): 건너뛸 개수
        limit (int): 최대 개수
        db (Session): 데이터베이스 세션

    Returns:
        list[Comment]: 댓글 리스트
    """
    controller = CommentController(db)
    return controller.get_comments_by_post(post_id, skip, limit)


@router.get("/{comment_id}", response_model=Comment, description="특정 댓글 조회")
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


@router.put("/{comment_id}", response_model=Comment, description="댓글 수정 (작성자만 가능)")
def update_comment(
    comment_id: int = Path(..., description="수정할 댓글 ID"),
    comment_data: CommentUpdate = Body(...),
    author_id: int = Query(..., description="작성자 ID (권한 확인용)"),
    db: Session = Depends(get_db)
):
    """댓글 수정

    Args:
        comment_id (int): 댓글 ID
        comment_data (CommentUpdate): 수정할 댓글 정보
        author_id (int): 작성자 ID (권한 확인용)
        db (Session): 데이터베이스 세션

    Returns:
        Comment: 수정된 댓글

    Raises:
        HTTPException: 댓글이 존재하지 않거나 권한이 없을 경우
    """
    try:
        controller = CommentController(db)
        comment = controller.update_comment(comment_id, comment_data, author_id)
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


@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT, description="댓글 삭제 (작성자만 가능)")
def delete_comment(
    comment_id: int = Path(..., description="삭제할 댓글 ID"),
    author_id: int = Query(..., description="작성자 ID (권한 확인용)"),
    db: Session = Depends(get_db)
):
    """댓글 삭제

    Args:
        comment_id (int): 댓글 ID
        author_id (int): 작성자 ID (권한 확인용)
        db (Session): 데이터베이스 세션

    Raises:
        HTTPException: 댓글이 존재하지 않거나 권한이 없을 경우
    """
    try:
        controller = CommentController(db)
        comment = controller.delete_comment(comment_id, author_id)
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
