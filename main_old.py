from fastapi import FastAPI, status 
from pydantic import BaseModel
from typing import Optional 
from fastapi import HTTPException
from routers.items import router as items_router
from fastapi import Depends
from fastapi import Query 
from fastapi import Header

app = FastAPI()

class Users(BaseModel):
    name: str
    email: str
    age: int
    password: str
    phone: int 

class User(BaseModel):
    name: str
    age: int
    city: Optional[str] = None

class Address(BaseModel):
    city: str
    pincode: int 

class FullUser(BaseModel):
    user: User 
    address: Address

class SignupRequest(BaseModel):
    name: str
    email: str
    password: str
    phone: Optional[int]

class SignupResponse(BaseModel):
    name: str
    email: str
    message: str = "signup success" 

@app.get("/")
def home():
    return {"message": "Hello Chandra Babu! FastAPI is running 🚀"}

@app.get("/hello/{name}")
def say_hello(name: str):
    return {"message": f"Hello {name}, welcome to FastAPI! 🚀"}

@app.get("/greet", status_code=status.HTTP_200_OK)
def greet(name: str, age: int):
    return {"message": f"Hello {name}, you are {age} years old!"}

@app.post("/create-user")
def create_user(details: User):
    return {"message": "user created!", "data": details}

@app.post("/create-full-user")
def create_full_user(payload: FullUser):
    return {"message": "full user created!", "data": payload}

@app.post("/sign-up", response_model=SignupResponse)
def sign_up(payload: SignupRequest):
    return payload 

@app.post("/validate-age")
def validate_age(user: User):
    if user.age < 18:
        raise HTTPException(status_code = 400, detail = "Age must be 18 or above")
    return {"message": "Valid age", "data": user}

@app.post("/register")
def register(user: Users):
    if user.age < 18:
        raise HTTPException(status_code = 400, detail = "Age must be 18 or above")
    elif len(user.password) < 6:
        raise HTTPException(status_code = 422, detail = "Password too short")
    return {"message": "Registration successful", "data": user}

app.include_router(items_router)

def give_name():
    return "Chandra Babu"

@app.get("/hello-me")
def hello_me(name: str = Depends(give_name)):
    return {"message": f"Hello {name}"}

@app.get("/search")
def search(q: str):
    return {"query": q}

@app.get("/check-name")
def check_name(
    name: str =  Query(...,min_length = 3, max_length = 10)
    ):
    return {"name": name}

@app.get("/check-regex")
def check_regex(
    name: str = Query(...,regex = "^[A-Za-z]+$")
    ):
    return {"name": name}

@app.get("/optional")
def optional_query(
    q: Optional[str] = Query(default=None)
    ):
    if q is None:
        return {"message": "No query given"}
    return {"query": q}

@app.get("/filer")
def filter_items(
    q: list[str] = Query(default = [])
    ):
    return {"query": q}

def common_params(q: str = None):
    return {"query": q}

@app.get("/products")
def get_products(commons: dict = Depends(common_params)):
    return {"message": "Products list", "data": commons}

@app.get("/order")
def get_orders(commons: dict = Depends(common_params)):
      return {"message": "Orders list", "data": commons}

API_KEY = "mysecretkey"

def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(401, "Invalid or missing API Key")
    return True

@app.get("/secure-data")
def secure_data(auth: bool = Depends(verify_api_key)):
    return {"message": "Access granted 🔥", "data": "secret info here"}






