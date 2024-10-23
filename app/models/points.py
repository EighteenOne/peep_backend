import uuid

from sqlalchemy import String, Column, func, DateTime, Text

from app.config.database import Base


class Point(Base):
    __tablename__ = "point"

    id = Column(String(36), default=lambda: str(uuid.uuid4()), primary_key=True)

    point = Column(String(128), index=True)
    access_key = Column(String(130))
    mobile_key = Column(String(130))
