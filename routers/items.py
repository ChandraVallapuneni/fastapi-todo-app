from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(
    prefix = "/items",
    tags = ["items"]
)

items_db = []

class Item(BaseModel):
    name: str 

@router.post("/")
def create_item(item: Item):
    new_id = len(items_db)+1
    new_item = {"id": new_id, **item.dict()}
    items_db.append(new_item)
    return {"message": "Item created", "item": new_item}

@router.get("/")
def get_items():
    return items_db 
    
@router.get("/{item_id}")
def get_item_by_id(item_id: int):
    for item in items_db:
        if item["id"] == item_id:
            return item
    return HTTPException(404, "Item not found")

@router.put("/{item_id}")
def update_item(item_id: int, item: Item):
    for db_item in items_db:
        if db_item["id"] == item_id:
            db_item["name"] = item.name 
            return item 
    raise HTTPException(404, "Item not found")

@router.delete("/{item_id}")
def delete_item(item_id: int):
    for index, db_item in enumerate(items_db):
        if db_item["id"] == item_id:
            deleted = items_db.pop(index)
            return {"message": "Item deleted", "item": deleted}
    raise HTTPException(404, "Item not found")