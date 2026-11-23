import requests


class IpService:
    """Получение IP-адреса и геоданных по нему."""

    IPIFY_URL = "https://api.ipify.org?format=json"
    IPINFO_URL = "https://ipinfo.io/{ip}/json"

    def get_ip(self) -> str:
        """Возвращает публичный IP-адрес пользователя."""
        response = requests.get(self.IPIFY_URL, timeout=10)
        response.raise_for_status()
        return response.json()["ip"]

    def get_geo_info(self, ip: str) -> dict:
        """Возвращает словарь с геоданными по IP-адресу."""
        url = self.IPINFO_URL.format(ip=ip)
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
