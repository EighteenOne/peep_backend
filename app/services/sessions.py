from typing import Type

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.sessions import PeepSession
from app.repositories.sessions import SessionRepository
from app.schemas.sessions import SessionInput


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

    def update(self, session: Type[PeepSession]):
        return self.repository.update(session)

    def get_path(self, session: Type[PeepSession]):
        return
