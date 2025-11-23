from fastapi import FastAPI 

from todo_app.routers.todos import router as todo_router

app = FastAPI()

app.include_router(todo_router)