import json
import os

from ip_service import IpService
from yandex_disk_service import YandexDiskService


def load_token(path: str = "token.txt") -> str:
    """Читает OAuth-токен Яндекс.Диска из файла."""
    with open(path, "r", encoding="utf-8") as f:
        return f.read().strip()


def main() -> None:
    token = load_token()
    ip_service = IpService()
    disk_service = YandexDiskService(token)

    # 1. IP и геоданные
    ip = ip_service.get_ip()
    geo_info = ip_service.get_geo_info(ip)
    print(f"IP: {ip}, город: {geo_info.get('city', 'неизвестен')}")

    # 2. Сохраняем в локальный JSON
    json_filename = "ip_info.json"
    with open(json_filename, "w", encoding="utf-8") as f:
        json.dump(geo_info, f, ensure_ascii=False, indent=2)

    # 3. Загружаем на Яндекс.Диск в отдельную папку
    folder = "/ip_detector"
    disk_service.create_folder(folder)
    disk_service.upload_file(json_filename, f"{folder}/{json_filename}")
    print(f"Файл {json_filename} загружен в {folder}")

    # 4. Чистим локальный файл, чтобы не оставался на компьютере
    os.remove(json_filename)


if __name__ == "__main__":
    main()
