from fastapi import APIRouter
from typing import Union
router = APIRouter()

@router.get("/")
def first_test():
    return {"Hello": "World 2 "}

@router.get("/article/{article_id}")
def read_article(article_id: int):
    return {"article_id": article_id}

@router.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@router.post("/article/")
def create_article(name: str, description: str, price: float):
    return {"name": name, "description": description, "price": price}