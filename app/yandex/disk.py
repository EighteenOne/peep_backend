import logging

import yadisk
from yadisk.exceptions import PathNotFoundError, ForbiddenError, WrongResourceTypeError

from app.config.settings import settings

logger = logging.getLogger(__name__)


class YadiskException(Exception):
    pass


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
        try:
            ld = self.client.listdir(path)
            return len(list(ld))
        except (PathNotFoundError, ForbiddenError, WrongResourceTypeError) as exc:
            logger.debug(f"Yandex disk api error: {exc}")
            raise YadiskException(exc)

    def create_folder(self, path: str) -> bool:
        self.client.mkdir(path)
        return True


yandex_disk_client = YandexDiskClient(settings.YANDEX_DISK_TOKEN)
