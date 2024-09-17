import logging

from fastapi import APIRouter, Request
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.schemas.points import PointInput
from app.services.point import PointService
from app.services.template import TemplateService

logger = logging.getLogger(__name__)

sentry_router = APIRouter(
    prefix="/sentry",
    tags=["sentry"]
)


@sentry_router.post("", status_code=200)
async def sentry_handler(
        request: Request
):
    payload = await request.json()
    # payload = await request.json()
    logger.info(payload)
    print(payload)
    return "ok"
