import requests


class YandexDiskService:
    """Работа с REST API Яндекс.Диска."""

    BASE_URL = "https://cloud-api.yandex.net/v1/disk/resources"

    def __init__(self, token: str):
        self.headers = {"Authorization": f"OAuth {token}"}

    def create_folder(self, folder_path: str) -> None:
        """Создаёт папку на Диске. 409 — папка уже есть, это не ошибка."""
        response = requests.put(
            self.BASE_URL,
            headers=self.headers,
            params={"path": folder_path},
            timeout=10,
        )
        if response.status_code not in (201, 409):
            response.raise_for_status()

    def upload_file(self, local_file: str, remote_path: str) -> None:
        """Загружает локальный файл на Диск по указанному пути."""
        response = requests.get(
            f"{self.BASE_URL}/upload",
            headers=self.headers,
            params={"path": remote_path, "overwrite": "true"},
            timeout=10,
        )
        response.raise_for_status()
        upload_url = response.json()["href"]

        with open(local_file, "rb") as f:
            upload_response = requests.put(upload_url, data=f, timeout=30)
            upload_response.raise_for_status()
