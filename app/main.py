from typing import Union
from fastapi import FastAPI
from app.api.main import router as api_router 
from sqlalchemy.orm import Session
from app.database import Base, engine

app = FastAPI()

app.include_router(api_router, prefix="/api")






