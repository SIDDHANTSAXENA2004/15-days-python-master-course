# from fastapi import FastAPI

# app = FastAPI()

# @app.get("/")
# def read_root():
#     return {"message": "Hello World! this is ur first api ."}

# @app.get("/goodbye")
# def read_goodbye():
#     return {"message": "Goodbye World! see u on day 9."}

# #user to give us data

# #path parameters
# #values that are part of url path
# #eg /users/123

# #query parameters
# #key value paira at the end of url eg ?role=admin

# #1.path parameters
# #{item_id}->variable /dynamic
# #:int -> type hint 
# @app.get("/items/{item_id}")
# def read_item(item_id:int):
#     return {"item_id":item_id,"description":f"Description of item {item_id}"}

# #2.query parameters
# #eg /search/?q=laptops
# @app.get("/search")
# def search_items(q:str):
#     return {"query":q,"results":["result1,result2"]}

from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

class Item(BaseModel):
    name:str
    price:float
    description:Optional[str]=None
    is_offer:Optional[bool]=None


app = FastAPI(
    title="FastAPI tutorial",
    description="day 8 tutorial",
    version="0.0.1",

)

@app.post("/items/")
def create_item(item:Item):
    print(f"Recived item: {item.name} , price: {item.price}")
    return {
        "message":f"Item '{item.name}' created successfully",
        "item_data":item
    }

@app.get("/")
def read_root():
    return {"message": "welcome to fastapi.go to /docs to get started"}