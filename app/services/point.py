from typing import Type

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.points import Point
from app.repositories.points import PointRepository
from app.schemas.points import PointInput, PointLogin
from app.utils import hashing_password


class PointService:

    def __init__(self, db: Session):
        self.repository = PointRepository(db)

    def create(self, data: PointInput) -> str:
        if self.repository.exists_by_name(data.point):
            raise HTTPException(status_code=400, detail="Point already exists")
        point = self.repository.create(data)
        return point.id

    def get_by_point(self, point: str):
        return self.repository.get_by_point(point)

    def is_key_valid(self, data: PointLogin) -> bool:
        point = self.repository.get_by_point(data.point)
        if point is None:
            return False
        return hashing_password.is_correct_password(point.mobile_key, data.key)

    def update(self, point: Type[Point]):
        return self.repository.update(point)
