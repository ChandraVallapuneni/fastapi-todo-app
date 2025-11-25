from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select 

from todo_app.database import get_db
from todo_app.models import Todo
from todo_app.schemas.todo_db_schema import TodoCreate, TodoUpdate, TodoResponse

router = APIRouter(prefix="/dbtodos",tags =["DB Todos"])

@router.post("/",response_model=TodoResponse, status_code = 201)
async def create_todo(todo: TodoCreate, session: AsyncSession = Depends(get_db)):
    new_todo = Todo(title=todo.title, user_id=todo.user_id)

    session.add(new_todo)
    await session.commit()
    await session.refresh(new_todo)

    return new_todo

@router.get("/", response_model=list[TodoResponse])
async def get_all_todos(session: AsyncSession = Depends(get_db),
            limit: int = 10,
            offset: int = 0 ):
    result = await session.execute(select(Todo).limit(limit).offset(offset))
    todos = result.scalars().all()

    return todos

@router.get("/{todo_id}",response_model=TodoResponse)
async def get_todo(todo_id: int, session: AsyncSession = Depends(get_db)):
    result = await session.execute(
        select(Todo).where(Todo.id == todo_id)
    )
    todo = result.scalar_one_or_none()

    if not todo:
        raise HTTPException(404,"Todo not found")
    return todo

@router.put("/{todo_id}",response_model=TodoResponse)
async def update_todo(todo_id: int, todo_data: TodoUpdate,session: AsyncSession = Depends(get_db)):
    # 1. Fetch existing todo
    result = await session.execute(
        select(Todo).where(Todo.id == todo_id)
    )
    todo = result.scalar_one_or_none()

    if not todo:
        raise HTTPException(404, "Todo not found")

    # Apply only provided fields
    if todo_data.title is not None:
        todo.title = todo_data.title
    if todo_data.completed is not None:
        todo.completed = todo_data.completed

    # 3. Commit changes
    await session.commit()
    await session.refresh(todo)

    # 4. Return updated todo
    return todo

@router.delete("/{todo_id}", status_code=204)
async def delete_todo(todo_id: int, session: AsyncSession = Depends(get_db)):

    # 1. Find the todo
    result = await session.execute(
        select(Todo).where(Todo.id == todo_id)
    )
    todo = result.scalar_one_or_none()

    if not todo:
        raise HTTPException(404, "Todo not found")

    # 2. Delete the todo
    await session.delete(todo)

    # 3. Commit the change
    await session.commit()

    # 4. Return nothing
    return
