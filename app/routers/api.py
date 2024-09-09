from fastapi import APIRouter, Depends

from app.auth.auth import check_api_key
from app.routers.v1 import session

router = APIRouter(
    prefix="/v1"
)

router.include_router(
    session.router,
    dependencies=[Depends(check_api_key)]
)
