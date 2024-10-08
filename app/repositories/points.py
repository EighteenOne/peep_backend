from typing import Type

from sqlalchemy.orm import Session

from app.models.points import Point
from app.schemas.points import PointInput


class PointRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, data: PointInput):
        point = Point(**data.model_dump(exclude_none=True))
        self.db.add(point)
        self.db.commit()
        self.db.refresh(point)
        return point

    def get_by_point(self, point: str) -> Type[Point]:
        point = self.db.query(Point).filter_by(point=point).first()
        return point

    def exists_by_name(self, point: str) -> bool:
        point = self.db.query(Point).filter_by(point=point).first()
        return bool(point)
