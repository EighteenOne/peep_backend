import logging

from fastapi import APIRouter, Depends
from requests import Request
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
def sentry_handler(
        request: Request
):
    logger.info(request.json())
    return "ok"
