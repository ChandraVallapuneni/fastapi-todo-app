from fastapi import APIRouter, HTTPException
from todo_app.schemas.todo import Todo, TodoResponse

db = {}
counter = 1

router = APIRouter(prefix="/todos", tags = ["Todos"])

@router.post("/",response_model=TodoResponse,status_code=201)
def create_todo(todo: Todo):
    global counter
    new_todo = {"id": counter, **todo.dict()}
    db[counter] = new_todo
    counter+=1
    return new_todo 

@router.get("/",response_model = list[TodoResponse])
def get_all_todos():
    return list(db.values())

@router.get("/{todo_id}",response_model=TodoResponse)
def get_todo(todo_id: int):
    if todo_id not in db:
        raise HTTPException(404,"Todo not found")
    return db[todo_id]

@router.put("/{todo_id}",response_model=TodoResponse)
def update_todo(todo_id: int, todo: Todo):
    if todo_id not in db:
        raise HTTPException(404,"Todo not found")
    db[todo_id].update(todo.dict())
    return db[todo_id]

@router.delete("/{todo_id}",status_code = 204)
def delete_todo(todo_id: int):
    if todo_id not in db:
        raise HTTPException(404,"Todo not found")
    del db[todo_id]
    return 
    
     




