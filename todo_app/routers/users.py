from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from todo_app.database import get_db
from todo_app.models import User, Todo
from todo_app.schemas.todo_db_schema import UserCreate, UserResponse

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserResponse, status_code=201)
async def create_user(user: UserCreate, session: AsyncSession = Depends(get_db)):
    result = await session.execute(select(User).where(User.email == user.email))
    existing = result.scalar_one_or_none()

    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(email=user.email, password=user.password)
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    return new_user

@router.get("/{user_id}/todos")
async def get_user_todos(user_id: int, session: AsyncSession = Depends(get_db)):
    # 1. Check if user exists
    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(404, "User not found")

    # 2. Explicitly load all todos for this user
    result = await session.execute(
        select(Todo).where(Todo.user_id == user_id)
    )

    todos = result.scalars().all()
    return todos
