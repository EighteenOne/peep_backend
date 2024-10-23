from typing import Type

from sqlalchemy.orm import Session

from app.models.points import Point
from app.schemas.points import PointInput
from app.utils import hashing_password


class PointRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, data: PointInput):
        point = Point(**data.model_dump(exclude_none=True))
        point.access_key = hashing_password.hash_password(point.access_key)
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

    def update(self, point: Type[Point]):
        self.db.add(point)
        self.db.commit()
        self.db.refresh(point)
        return point
