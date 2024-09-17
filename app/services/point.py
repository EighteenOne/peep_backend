from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.points import PointRepository
from app.repositories.templates import TemplateRepository
from app.schemas.points import PointInput


class PointService:

    def __init__(self, db: Session):
        self.repository = PointRepository(db)

    def create(self, data: PointInput) -> str:
        if self.repository.exists_by_name(data.point):
            raise HTTPException(status_code=400, detail="Point already exists")
        point = self.repository.create(data)
        return point.id
