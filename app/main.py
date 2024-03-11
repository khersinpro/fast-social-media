from typing import Union
from fastapi import FastAPI
from app.api.main import router as api_router 

app = FastAPI()

app.include_router(api_router, prefix="/api")



