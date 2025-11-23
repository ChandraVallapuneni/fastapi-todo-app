from pydantic import BaseModel, Field

class Todo(BaseModel):
    title: str = Field(...,min_length = 3)
    description: str = Field(...,min_length = 5)
    completed: bool = False

class TodoResponse(Todo):
    id: int
