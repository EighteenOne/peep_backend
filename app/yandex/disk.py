import logging

import yadisk
from yadisk.exceptions import PathNotFoundError, ForbiddenError, WrongResourceTypeError

from app.config.settings import settings

logger = logging.getLogger(__name__)


class YandexDiskClient:

    def __init__(self, token):
        self.client = yadisk.Client(token=token)
        # self.disk_name = disk_name

    def publish(self, path: str) -> bool:
        self.client.publish(path)
        return True

    def get_public_link(self, path: str) -> str:
        meta = self.client.get_meta(path)
        return meta.public_url

    def get_count_files(self, path: str) -> int:
        rv = 0
        try:
            ld = self.client.listdir(path)
            rv = len(list(ld))
        except (PathNotFoundError, ForbiddenError, WrongResourceTypeError) as exc:
            logger.error("Yandex disk api error:", exc)
        return rv


yandex_disk_client = YandexDiskClient(settings.YANDEX_DISK_TOKEN)
