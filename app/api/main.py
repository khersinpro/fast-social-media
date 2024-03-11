from fastapi import APIRouter
from app.api.routes import test as test_router

router = APIRouter()

router.include_router(test_router.router, tags=["test"])
