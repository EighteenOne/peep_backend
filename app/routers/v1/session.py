from typing import Annotated

from app.schemas.sessions import SessionInput
from app.services.sessions import SessionService
from app.config.database import get_db
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/session",
    tags=["session"]
)


@router.post("", status_code=201)
def create_session(
        data: Annotated[SessionInput, Depends()], db_session: Session = Depends(get_db)
):
    """
    Create a new city.

    Args:
        data (CityInput): City data to be created.
        db_session (Session, optional): Database session. Defaults to Depends(get_db).

    Returns:
        CityOutput: Created city.
    """
    _service = SessionService(db_session)
    return _service.create(data)
