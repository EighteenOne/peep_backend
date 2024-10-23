import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.schemas.points import PointInput, PointLogin
from app.services.point import PointService
from app.services.template import TemplateService

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/point",
    tags=["point"]
)


@router.post("", status_code=201)
def create_point(
        data: PointInput, db_session: Session = Depends(get_db)
):
    service = PointService(db_session)
    rv = service.create(data)

    template_service = TemplateService(db_session)
    template_service.create_default(data.point)

    logger.info(f"Point created {rv} from {data.model_dump()}")
    return rv


@router.post("/login", status_code=200)
def login(
        data: PointLogin, db_session: Session = Depends(get_db)
):
    service = PointService(db_session)
    rv = service.is_key_valid(data)
    if not rv:
        raise HTTPException(status_code=401, detail="Point or key invalid")
    return rv
