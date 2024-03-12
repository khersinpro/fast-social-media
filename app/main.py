from typing import Union
from fastapi import FastAPI
from app.api.main import router as api_router 
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine

#import all models from folder models
from app.api.models import user

# Create all tables in the database
def create_tables():
    user.Base.metadata.create_all(bind=engine)

create_tables()

app = FastAPI()


app.include_router(api_router, prefix="/api")






