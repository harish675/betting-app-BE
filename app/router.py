from fastapi import APIRouter ,Depends
from .users.routes import router as user_router
from .auth.routes import router as auth_router
from .auth.routes import user_router as auth_user_router
from ..core.middleware.middleware import authentication
router = APIRouter()

@router.get("/health")
async def health_check():
    return {"status": "healthy"}

router.include_router(auth_user_router, prefix="/auth", tags=["auth"])

router.include_router(user_router, prefix="/users", tags=["users"])

router.include_router(auth_router, prefix="/auth", tags=["auth"],dependencies=[Depends(authentication)])