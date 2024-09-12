import logging

import yadisk

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
        try:
            ld = self.client.listdir(path)
        except yadisk.exceptions.PathNotFoundError as exc:
            logger.error("Yandex disk api error:", exc)
            return 0

        return len(list(ld))


yandex_disk_client = YandexDiskClient(settings.YANDEX_DISK_TOKEN)
