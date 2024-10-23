import logging
from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.schemas.sessions import SessionInput, CloseSessionInput, GetWaitingSessionsInput, GetWaitingSessionsOutput
from app.services.session import SessionService
from app.yandex.disk import yandex_disk_client

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/session",
    tags=["session"]
)


@router.post("", status_code=201)
def create_session(
        data: SessionInput, db_session: Session = Depends(get_db)
):
    service = SessionService(db_session)
    rv = service.create(data)
    logger.info(f"Session created {rv} from {data.model_dump()}")
    return rv


# need only for tilda webhook registration
# @router.post("/waiting/create")
# def create_waiting_session():
#     return "OK"

# curl -X 'POST' 'http://0.0.0.0:8000/peep/api/v1/session/waiting/create' -H 'content-length: 304' -H 'content-type: application/x-www-form-urlencoded' -H 'referer: https://peep-picture.ru/peep1' -H 'accept: */*' -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36' -H 'host: webhook.site' -d $'name=%D0%9C%D0%B8%D1%85%D0%B0%D0%B8%D0%BB%D0%A2%D0%B5%D1%81%D1%82&email=mikhail%40gmail.com&Checkbox=yes&mail_template=Peep&point=peep1&tranid=8005343%3A6768654971&formid=form803070350&formname=%D0%B0%D0%BD%D0%BA%D0%B5%D1%82%D0%B0+peep'
@router.post("/waiting/create")
def create_waiting_session(
        point: str = Form(...),
        email: str = Form(...),
        name: str = Form(...),
        db_session: Session = Depends(get_db)):
    date_str = datetime.utcnow().strftime('%d.%m.%Y')
    time_str = datetime.utcnow().strftime('%H-%M')

    session_name = f"{name} - {date_str} {time_str}"

    session_input = SessionInput(
        count_photos=0,
        datetime_str=date_str,
        email=email,
        name=name,
        point=point,
        session=session_name,
        status=10
    )

    # peep1/username - 26.10.2023 22-23
    folder_name = f"{point}/{session_name}"
    yandex_disk_client.create_folder(folder_name)

    service = SessionService(db_session)
    rv = service.create(session_input)
    logger.info(f"Session created {rv}")
    return rv


@router.post("/waiting/get", status_code=200, response_model=List[GetWaitingSessionsOutput])
def get_waiting_sessions(
        data: GetWaitingSessionsInput, db_session: Session = Depends(get_db)
):
    service = SessionService(db_session)
    rv = service.get_waiting_by_point(data.point)
    return rv


@router.post("/close", status_code=200)
def close_session(
        data: CloseSessionInput, db_session: Session = Depends(get_db)
):
    service = SessionService(db_session)

    session = service.get_by_session_name(data.session)

    session.count_photos = data.count_photos
    session.status = 0

    service.update(session)
