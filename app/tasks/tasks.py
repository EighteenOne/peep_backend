import datetime
from logging import Logger

from app.config.database import SessionLocal
from app.notification.email import email_service
from app.repositories.points import PointRepository
from app.schemas.points import PointInput
from app.schemas.templates import TemplateInput
from app.services.sessions import SessionService
from app.services.templates import TemplateService
from app.yandex.disk import yandex_disk_client, YadiskException


def update_uploaded_count_photos(logger: Logger) -> None:
    log_task_name = "update_uploaded_count_photos"

    logger.info(f"[{log_task_name}] Started task")

    db = SessionLocal()

    session_service = SessionService(db)
    new_sessions = session_service.get_by_status(0)
    logger.info(f"[{log_task_name}] Found {len(new_sessions)} sessions with status {0}")

    for peep_session in new_sessions:
        log_session = peep_session.session

        logger.info(f"[{log_task_name}][{log_session}] Processing session")

        path = peep_session.get_path()
        try:
            actual_count = yandex_disk_client.get_count_files(path)
        except YadiskException as exc:
            logger.error(f"[{log_task_name}][{log_session}] Got yandex disk api exception for path {path}: {exc}")
            continue

        logger.info(f"[{log_task_name}][{log_session}] Found {actual_count}/{peep_session.count_photos} files at disk")

        if actual_count == peep_session.count_photos:
            yandex_disk_client.publish(path)
            public_link = yandex_disk_client.get_public_link(path)

            logger.info(f"[{log_task_name}][{log_session}] Got public link {public_link}")

            peep_session.status = 1
            peep_session.public_link = public_link
            peep_session.count_photos_cloud = peep_session.count_photos
        else:
            peep_session.count_photos_cloud = actual_count

        session_service.update(peep_session)

    db.close()
    logger.info(f"[{log_task_name}] Task finished, db conn closed")


def send_emails(logger: Logger) -> None:
    log_task_name = "send_emails"

    logger.info(f"[{log_task_name}] Started task")
    db = SessionLocal()
    session_service = SessionService(db)
    template_service = TemplateService(db)

    new_sessions = session_service.get_by_status(1)
    logger.info(f"[{log_task_name}] Found {len(new_sessions)} sessions with status {1}")

    for peep_session in new_sessions:
        log_session = peep_session.session
        logger.info(f"[{log_task_name}][{log_session}] Processing session")

        template = template_service.get_by_point(peep_session.point)
        if template is None:
            logger.error(f"[{log_task_name}][{log_session}] Template not found for point {peep_session.point}")
            continue

        msg = template.template_text
        msg = msg.replace("[Имя]", peep_session.name)
        msg = msg.replace("[Ссылка]", peep_session.public_link)

        try:
            email_service.send_mail(msg, template.subject, peep_session.email)
        except Exception as exc:
            logger.error(f"[{log_task_name}][{log_session}] Send email error", exc)
            continue

        peep_session.status = 2
        peep_session.sent_at = datetime.datetime.now()
        session_service.update(peep_session)

    db.close()
    logger.info(f"[{log_task_name}] Task finished, db conn closed")


def create_point():
    db = SessionLocal()
    repo = PointRepository(db)

    repo.create(
        PointInput(point="peep1", key='secret'))
    db.close()


def create_template():
    db = SessionLocal()
    template_service = TemplateService(db)

    template = '''
Привет! На связи фото-трельяж Peep    

Ваши фотографии готовы и доступны для скачивания по ссылке: [Имя] - [Ссылка]

Как сохранять фото так, чтобы не терялось качество?
https://peep-picture.ru/save_pic

Внимание 👀 Фотографии будут доступны для скачивания только 7 дней, информация даже в облаке загрязняет планету, не забудьте их скачать!

Будем рады вашим отметкам в соц сетях и обратной связи в директ!

Если вы хотите сделать ваше событие незабываемым, можете приобрести или арендовать трельяж Peep - подробная информация на сайте:
https://peep-global.com
'''

    template_service.create(
        TemplateInput(point="peep1", subject="Peep! Это тестовая версия письма", template_text=template))
    db.close()
