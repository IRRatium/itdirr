from __future__ import annotations
import requests


def download_banner(client, username: str, path: str) -> str | None:
    """
    Скачать баннер пользователя и сохранить в файл.
    Возвращает путь к файлу или None если баннера нет.
    """
    from ..api.users import get_user

    user = get_user(client, username)

    if not user.banner:
        return None

    response = requests.get(user.banner, timeout=30)
    response.raise_for_status()

    with open(path, "wb") as f:
        f.write(response.content)

    return path
