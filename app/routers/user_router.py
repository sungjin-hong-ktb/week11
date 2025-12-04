from fastapi import APIRouter, Depends, HTTPException, status, Path, Body
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.user_schema import UserCreate, UserUpdate, User
from app.controllers.user_controller import UserController

router = APIRouter(
    prefix="/api/users",
    tags=["users"],
)

# Create user
@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED, description="새로운 사용자 생성")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        controller = UserController(db)
        return controller.create_user(user)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

# Get users
@router.get("/", response_model=list[User], status_code=status.HTTP_200_OK, description="모든 사용자 목록 조회")
def get_users(db: Session = Depends(get_db)):
    controller = UserController(db)
    return controller.get_users()

# Get user by id
@router.get("/{user_id}", response_model=User, status_code=status.HTTP_200_OK, description="특정 사용자 조회")
def get_user(user_id: int = Path(..., description="조회할 사용자 ID"), db: Session = Depends(get_db)):
    controller = UserController(db)
    user = controller.get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="사용자를 찾을 수 없습니다")
    return user

# Update user by id
@router.put("/{user_id}", response_model=User, status_code=status.HTTP_200_OK, description="사용자 정보 수정")
def update_user(
    user_id: int = Path(..., description="수정할 사용자 ID"),
    user: UserUpdate = Body(...),
    db: Session = Depends(get_db)
):
    try:
        controller = UserController(db)
        result = controller.update_user(user_id, user)
        if result is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="사용자를 찾을 수 없습니다")
        return result
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

# Delete user by id
@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT, description="사용자 삭제")
def delete_user(user_id: int = Path(..., description="삭제할 사용자 ID"), db: Session = Depends(get_db)):
    controller = UserController(db)
    user = controller.delete_user(user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="사용자를 찾을 수 없습니다")
    return None
