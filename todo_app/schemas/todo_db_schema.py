from pydantic import BaseModel

# Schema for creating a new Todo (POST)
class TodoCreate(BaseModel):
    title: str
    user_id: int

# Schema for updating a Todo (PUT)
class TodoUpdate(BaseModel):
    title: str | None = None
    completed: bool | None = None

# Schema for API responses
class TodoResponse(BaseModel):
    id: int
    title: str
    completed: bool
    user_id: int

class UserCreate(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    email: str

    class Config:
        from_attributes = True

