from fastapi import APIRouter
from app.api.routes import user, role, post, comment, like 

router = APIRouter()

router.include_router(user.router, tags=["users"], prefix="/users")
router.include_router(role.router, tags=["roles"], prefix="/roles")
router.include_router(post.router, tags=["posts"], prefix="/posts")
router.include_router(comment.router, tags=["comments"], prefix="/comments")
router.include_router(like.router, tags=["likes"], prefix="/likes")


