from fastapi import APIRouter

from .auth import router as auth_router

router = APIRouter(prefix="/v1")

# include more routers here...
router.include_router(auth_router)
