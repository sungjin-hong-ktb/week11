from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.post_schema import Post, PostCreate, PostUpdate, PostDetail
from app.controllers.post_controller import PostController

router = APIRouter(
    prefix="/posts",
    tags=["posts"]
)


@router.post("/", response_model=Post, status_code=status.HTTP_201_CREATED)
def create_post(
    post_data: PostCreate,
    author_id: int,
    db: Session = Depends(get_db)
):
    """게시글 생성

    Args:
        post_data (PostCreate): 생성할 게시글 정보
        author_id (int): 작성자 ID
        db (Session): 데이터베이스 세션

    Returns:
        Post: 생성된 게시글
    """
    controller = PostController(db)
    return controller.create_post(post_data, author_id)


@router.get("/", response_model=list[Post])
def get_posts(
    skip: int = 0,
    limit: int = 100,
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


@router.get("/{post_id}", response_model=PostDetail)
def get_post(
    post_id: int,
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


@router.put("/{post_id}", response_model=Post)
def update_post(
    post_id: int,
    post_data: PostUpdate,
    author_id: int,
    db: Session = Depends(get_db)
):
    """게시글 수정

    Args:
        post_id (int): 게시글 ID
        post_data (PostUpdate): 수정할 게시글 정보
        author_id (int): 작성자 ID (권한 확인용)
        db (Session): 데이터베이스 세션

    Returns:
        Post: 수정된 게시글

    Raises:
        HTTPException: 게시글이 존재하지 않거나 권한이 없을 경우
    """
    try:
        controller = PostController(db)
        post = controller.update_post(post_id, post_data, author_id)
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


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    post_id: int,
    author_id: int,
    db: Session = Depends(get_db)
):
    """게시글 삭제

    Args:
        post_id (int): 게시글 ID
        author_id (int): 작성자 ID (권한 확인용)
        db (Session): 데이터베이스 세션

    Raises:
        HTTPException: 게시글이 존재하지 않거나 권한이 없을 경우
    """
    try:
        controller = PostController(db)
        post = controller.delete_post(post_id, author_id)
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
