from typing import Type

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.templates import Template
from app.repositories.templates import TemplateRepository
from app.schemas.templates import TemplateInput


class TemplateService:

    def __init__(self, db: Session):
        self.repository = TemplateRepository(db)

    def create(self, data: TemplateInput) -> str:
        if self.repository.exists_by_point(data.point):
            raise HTTPException(status_code=400, detail="Template already exists")
        template = self.repository.create(data)
        return template.id

    def get_by_point(self, point: str):
        return self.repository.get_by_point(point)

    def update(self, template: Type[Template]):
        return self.repository.update(template)
