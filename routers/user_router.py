from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from schemas.user_schema import UserCreate, UserUpdate, User
from controllers import user_controller

router = APIRouter(
    prefix="/api/users",
    tags=["users"],
)

# Create user
@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        return user_controller.create_user(db, user)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

# Get users
@router.get("/", response_model=list[User], status_code=status.HTTP_200_OK)
async def get_users(db: Session = Depends(get_db)):
    return user_controller.get_users(db)

# Get user by id
@router.get("/{user_id}", response_model=User, status_code=status.HTTP_200_OK)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    user = user_controller.get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="사용자를 찾을 수 없습니다")
    return user

# Update user by id
@router.put("/{user_id}", response_model=User, status_code=status.HTTP_200_OK)
async def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    try:
        result = user_controller.update_user(db, user_id, user)
        if result is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="사용자를 찾을 수 없습니다")
        return result
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

# Delete user by id
@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = user_controller.delete_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="사용자를 찾을 수 없습니다")
    return None
