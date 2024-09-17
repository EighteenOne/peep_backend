from fastapi import APIRouter, Depends

from app.auth.auth import check_api_key
from app.routers.v1 import session, root, point

router = APIRouter(
    prefix="/api/v1",
    dependencies=[Depends(check_api_key)]
)

router.include_router(
    session.router,
)
router.include_router(
    root.router,
)
router.include_router(
    point.router,
)
