from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from todo_app.routers.todos import router as todo_router        # old CRUD (dictionary)
from todo_app.routers.todos_db import router as tododb_router  # new CRUD (SQLAlchemy)
from todo_app.routers.users import router as users_router

from todo_app.database import get_db

from todo_app.database import init_db

app = FastAPI()

app.include_router(todo_router)     # /todos → dictionary version
app.include_router(tododb_router)   # /dbtodos → SQLAlchemy version
app.include_router(users_router)

@app.get("/test-db")
async def test_db(session: AsyncSession = Depends(get_db)):
    try:
        await session.execute(text("SELECT 1"))
        return {"status": "Database connected successfully!"}
    except Exception as e:
        return {"error": str(e)}

@app.on_event("startup")
async def on_startup():
    await init_db()
