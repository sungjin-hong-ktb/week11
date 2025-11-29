from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from schemas import UserCreate, UserUpdate

router = APIRouter(
    prefix="/api/users",
)

# Create user
@router.post("/")
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    pass

# Get users
@router.get("/")
async def get_users(db: Session = Depends(get_db)):
    pass

# Get user by id
@router.get("/{user_id}")
async def get_user(user_id: int, db: Session = Depends(get_db)):
    pass

# Update user by id
@router.put("/{user_id}")
async def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    pass

# Delete user by id 
@router.delete("/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    pass