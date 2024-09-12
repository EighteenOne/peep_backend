import uuid

from sqlalchemy import String, Column, func, DateTime, Integer

from app.config.database import Base


class PeepSession(Base):
    __tablename__ = "session"
    id = Column(String(36), default=lambda: str(uuid.uuid4()), primary_key=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    count_photos = Column(Integer)
    datetime_str = Column(String(25))
    email = Column(String(128))
    name = Column(String(128))
    point = Column(String(128), index=True)
    session = Column(String(128))

    status = Column(Integer, index=True, default=0)
    count_photos_cloud = Column(Integer)
    public_link = Column(String(512))
    sent_at = Column(DateTime)

    def get_path(self):
        return f"Peep/{self.point}/{self.session}"
