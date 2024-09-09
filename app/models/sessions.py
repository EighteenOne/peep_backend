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

# count_photos
# datetime
# email
# name
# point
# session

# TODO: вопросы
# 1. нужен ли ip


# 1	id Первичный	int(11)			Нет	Нет		AUTO_INCREMENT
# 2	addtime	int(11)			Нет	Нет
# 3	ip	varchar(32)	utf8mb4_general_ci		Нет	Нет
# 4	session	varchar(128)	utf8mb4_general_ci		Нет	Нет
# 5	mailbox_from	int(11)			Нет	0
# 6	template	int(11)			Нет	0
# 7	name	varchar(128)	utf8mb4_general_ci		Нет	Нет
# 8	date	varchar(16)	utf8mb4_general_ci		Нет	Нет
# 9	time	varchar(16)	utf8mb4_general_ci		Нет	Нет
# 10	client_email	varchar(128)	utf8mb4_general_ci		Нет	Нет
# 11	cloud	varchar(128)	utf8mb4_general_ci		Нет	Нет
# 12	count_photos	int(11)			Нет	Нет
# 13	count_photos_cloud	int(11)			Нет	0
# 14	public_link	varchar(512)	utf8mb4_general_ci		Да	NULL
# 15	senttime	int(11)			Нет	0
# 16	status	int(11)			Нет	0	0 - пришло, 1 - получена ссылка, 2 - письмо отправлено
# 17	status_public	int(11)			Да	NULL	1 - убрана публичная ссылка, 2 - перенесено в корзину
