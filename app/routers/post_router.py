from fastapi import APIRouter, Depends, HTTPException, status, Query, Path, Body, Header
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.post_schema import Post, PostCreate, PostUpdate, PostDetail
from app.schemas.comment_schema import Comment, CommentCreate
from app.controllers.post_controller import PostController
from app.controllers.comment_controller import CommentController

router = APIRouter(
    prefix="/posts",
    tags=["posts"]
)


@router.post(
    "/",
    response_model=Post,
    status_code=status.HTTP_201_CREATED,
    description="새로운 게시글 작성"
)
def create_post(
    post_data: PostCreate = Body(...),
    x_user_id: int = Header(
        ...,
        alias="X-User-ID",
        description="작성자 ID"
    ),
    db: Session = Depends(get_db)
):
    """게시글 생성

    Args:
        post_data (PostCreate): 생성할 게시글 정보
        x_user_id (int): 헤더로 전달된 작성자 ID
        db (Session): 데이터베이스 세션

    Returns:
        Post: 생성된 게시글
    """
    controller = PostController(db)
    return controller.create_post(post_data, x_user_id)


@router.get(
    "/",
    response_model=list[Post],
    description="게시글 목록 조회 (댓글 개수 포함)"
)
def get_posts(
    skip: int = Query(0, ge=0, description="건너뛸 개수"),
    limit: int = Query(10, ge=1, le=100, description="최대 조회 개수"),
    db: Session = Depends(get_db)
):
    """모든 게시글 조회

    Args:
        skip (int): 건너뛸 개수
        limit (int): 최대 개수
        db (Session): 데이터베이스 세션

    Returns:
        list[Post]: 게시글 리스트
    """
    controller = PostController(db)
    return controller.get_posts(skip, limit)


@router.get(
    "/{post_id}",
    response_model=PostDetail,
    description="게시글 상세 조회 (댓글 포함, 조회수 증가)"
)
def get_post(
    post_id: int = Path(..., description="조회할 게시글 ID"),
    db: Session = Depends(get_db)
):
    """게시글 상세 조회 (댓글 포함, 조회수 증가)

    Args:
        post_id (int): 게시글 ID
        db (Session): 데이터베이스 세션

    Returns:
        PostDetail: 게시글 상세 정보 (댓글 포함)

    Raises:
        HTTPException: 게시글이 존재하지 않을 경우
    """
    controller = PostController(db)
    post = controller.get_post_by_id(post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="게시글을 찾을 수 없습니다"
        )
    return post


@router.put(
    "/{post_id}",
    response_model=Post,
    description="게시글 수정 (작성자만 가능)"
)
def update_post(
    post_id: int = Path(..., description="수정할 게시글 ID"),
    post_data: PostUpdate = Body(...),
    x_user_id: int = Header(
        ...,
        alias="X-User-ID",
        description="작성자 ID (권한 확인용)"
    ),
    db: Session = Depends(get_db)
):
    """게시글 수정

    Args:
        post_id (int): 게시글 ID
        post_data (PostUpdate): 수정할 게시글 정보
        x_user_id (int): 헤더로 전달된 작성자 ID (권한 확인용)
        db (Session): 데이터베이스 세션

    Returns:
        Post: 수정된 게시글

    Raises:
        HTTPException: 게시글이 존재하지 않거나 권한이 없을 경우
    """
    try:
        controller = PostController(db)
        post = controller.update_post(
            post_id,
            post_data,
            x_user_id
        )
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="게시글을 찾을 수 없습니다"
            )
        return post
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )


@router.delete(
    "/{post_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="게시글 삭제 (작성자만 가능)"
)
def delete_post(
    post_id: int = Path(..., description="삭제할 게시글 ID"),
    x_user_id: int = Header(
        ...,
        alias="X-User-ID",
        description="작성자 ID (권한 확인용)"
    ),
    db: Session = Depends(get_db)
):
    """게시글 삭제

    Args:
        post_id (int): 게시글 ID
        x_user_id (int): 헤더로 전달된 작성자 ID (권한 확인용)
        db (Session): 데이터베이스 세션

    Raises:
        HTTPException: 게시글이 존재하지 않거나 권한이 없을 경우
    """
    try:
        controller = PostController(db)
        post = controller.delete_post(post_id, x_user_id)
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="게시글을 찾을 수 없습니다"
            )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )


@router.get(
    "/{post_id}/comments",
    response_model=list[Comment],
    description="특정 게시글의 댓글 목록 조회"
)
def get_post_comments(
    post_id: int = Path(..., gt=0, description="게시글 ID"),
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


@router.post(
    "/{post_id}/comments",
    response_model=Comment,
    status_code=status.HTTP_201_CREATED,
    description="게시글에 새로운 댓글 작성"
)
def create_post_comment(
    post_id: int = Path(..., gt=0, description="게시글 ID"),
    comment_data: CommentCreate = Body(...),
    x_user_id: int = Header(
        ...,
        alias="X-User-ID",
        description="작성자 ID"
    ),
    db: Session = Depends(get_db)
):
    """게시글에 댓글 생성

    Args:
        post_id (int): 게시글 ID
        comment_data (CommentCreate): 생성할 댓글 정보
        x_user_id (int): 헤더로 전달된 작성자 ID
        db (Session): 데이터베이스 세션

    Returns:
        Comment: 생성된 댓글
    """
    controller = CommentController(db)
    # URL의 post_id를 우선 사용 (RESTful)
    return controller.create_comment(
        comment_data,
        post_id,
        x_user_id
    )
