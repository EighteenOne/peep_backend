from typing import Type

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.templates import Template
from app.repositories.templates import TemplateRepository
from app.schemas.templates import TemplateInput

DEFAULT_TEMPLATE = '''
Привет! На связи фото-трельяж Peep    

Ваши фотографии готовы и доступны для скачивания по ссылке: [Имя] - [Ссылка]

Как сохранять фото так, чтобы не терялось качество?
https://peep-picture.ru/save_pic

Внимание 👀 Фотографии будут доступны для скачивания только 7 дней, информация даже в облаке загрязняет планету, не забудьте их скачать!

Будем рады вашим отметкам в соц сетях и обратной связи в директ!

Если вы хотите сделать ваше событие незабываемым, можете приобрести или арендовать трельяж Peep - подробная информация на сайте:
https://peep-global.com
'''

DEFAULT_SUBJECT = "Привет! На связи фото-трельяж Peep"


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

    def create_default(self, point: str) -> str:
        if self.repository.exists_by_point(point):
            raise HTTPException(status_code=400, detail="Template already exists")
        template = self.repository.create(
            TemplateInput(point=point, subject=DEFAULT_SUBJECT, template_text=DEFAULT_TEMPLATE))
        return template.id
