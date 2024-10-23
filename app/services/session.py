from typing import Type

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.sessions import PeepSession
from app.repositories.sessions import SessionRepository
from app.schemas.sessions import SessionInput, GetWaitingSessionsOutput


class SessionService:

    def __init__(self, db: Session):
        self.repository = SessionRepository(db)

    def create(self, data: SessionInput) -> str:
        if self.repository.exists_by_name(data.session):
            raise HTTPException(status_code=400, detail="Session already exists")
        session = self.repository.create(data)
        return session.id

    def get_by_status(self, status: int):
        return self.repository.get_by_status(status)

    def get_by_session_name(self, session_name: str):
        return self.repository.get_by_session_name(session_name)

    def get_waiting_by_point(self, point: str):
        sessions = self.repository.get_by_point_with_status(point, 10)
        return [
            GetWaitingSessionsOutput(
                session=session.session,
                disk_path=f"{session.point}/{session.session}",
                email=session.email,
                datetime_str=session.datetime_str,
            ) for
            session in sessions
        ]

    def update(self, session: Type[PeepSession]):
        return self.repository.update(session)
