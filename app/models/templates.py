import uuid

from sqlalchemy import String, Column, func, DateTime, Text

from app.config.database import Base


class Template(Base):
    __tablename__ = "template"

    id = Column(String(36), default=lambda: str(uuid.uuid4()), primary_key=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    point = Column(String(128), index=True)
    subject = Column(String(128))
    template_text = Column(Text)
