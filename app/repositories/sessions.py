from typing import List, Type

from sqlalchemy.orm import Session

from app.models.sessions import PeepSession
from app.schemas.sessions import SessionInput, SessionOutput


class SessionRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, data: SessionInput) -> PeepSession:
        session = PeepSession(**data.model_dump(exclude_none=True))
        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)
        return session

    def exists_by_name(self, name: str) -> bool:
        session = self.db.query(PeepSession).filter_by(name=name).first()
        return bool(session)

    # def get_by_status(self, status: int) -> List[SessionOutput]:
    #     sessions = self.db.query(PeepSession).filter_by(status=status).all()
    #     return [SessionOutput.model_validate(session) for session in sessions]

    def get_by_status(self, status: int) -> List[Type[PeepSession]]:
        sessions = self.db.query(PeepSession).filter_by(status=status).all()
        return sessions

    def update(self, session: Type[PeepSession]):
        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)
        return session
