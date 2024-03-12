from fastapi import APIRouter
from app.api.routes import user 

router = APIRouter()

router.include_router(user.router, tags=["users"], prefix="/users")
