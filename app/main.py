from typing import Union
from fastapi import FastAPI
from app.api.main import router as api_router 
from sqlalchemy.orm import Session
from app.database import Base, engine

#import all models from folder models
from app.api.models import user
from app.api.models import role

# Create all tables in the database
def create_tables():
    Base.metadata.create_all(bind=engine)

create_tables()

app = FastAPI()


app.include_router(api_router, prefix="/api")






