import yadisk

from app.config.settings import settings


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
        # TODO except yadisk.exceptions.PathNotFoundError:
        ld = self.client.listdir(path)
        return len(list(ld))


yandex_disk_client = YandexDiskClient(settings.YANDEX_DISK_TOKEN)
