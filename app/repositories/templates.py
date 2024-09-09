from typing import List, Type

from sqlalchemy.orm import Session

from app.models.templates import Template
from app.schemas.templates import TemplateInput


class TemplateRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, data: TemplateInput):
        template = Template(**data.model_dump(exclude_none=True))
        self.db.add(template)
        self.db.commit()
        self.db.refresh(template)
        return template

    def exists_by_point(self, point: str) -> bool:
        template = self.db.query(Template).filter_by(point=point).first()
        return bool(template)

    def get_by_point(self, point: str) -> Type[Template]:
        template = self.db.query(Template).filter_by(point=point).first()
        return template

    def update(self, template: Type[Template]):
        self.db.add(template)
        self.db.commit()
        self.db.refresh(template)
        return template
