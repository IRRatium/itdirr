from __future__ import annotations


def view_post(client, post_id: str) -> bool:
    """
    Отметить пост как просмотренный.
    Сайт вызывает это автоматически при открытии поста.
    """
    response = client.post(f"/api/posts/{post_id}/view")
    return response.status_code in (200, 204)


def view_posts(client, post_ids: list[str]) -> dict[str, bool]:
    """
    Отметить несколько постов как просмотренные.
    Возвращает словарь {post_id: успех}.
    """
    return {pid: view_post(client, pid) for pid in post_ids}
