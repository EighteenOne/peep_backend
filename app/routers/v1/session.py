import logging

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.schemas.sessions import SessionInput
from app.services.session import SessionService

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/session",
    tags=["session"]
)


@router.post("", status_code=201)
def create_session(
        data: SessionInput, db_session: Session = Depends(get_db)
):
    _service = SessionService(db_session)
    rv = _service.create(data)
    logger.info(f"Session created {rv} from {data.model_dump()}")
    return rv
