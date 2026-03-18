from __future__ import annotations

from ..models import Posts, Post
from ._common import build_query


def get_wall(client, username: str, limit: int = 20, cursor: str | None = None) -> Posts:
    """Получить посты со стены пользователя."""
    params: dict = {"limit": limit}
    if cursor:
        params["cursor"] = cursor
    query = build_query(params)
    response = client.get(f"/api/posts/wall/{username}?{query}")
    response.raise_for_status()
    return Posts.model_validate(response.json())


def post_to_wall(client, username: str, content: str) -> Post:
    """Написать пост на стену пользователя."""
    # получаем ID пользователя
    user_resp = client.get(f"/api/users/{username}")
    user_resp.raise_for_status()
    recipient_id = user_resp.json().get("id")
    if not recipient_id:
        raise ValueError(f"Не удалось получить ID пользователя @{username}")

    payload = {
        "content": content,
        "attachmentIds": [],
        "wallRecipientId": recipient_id,
    }
    response = client.post("/api/posts", json=payload)
    response.raise_for_status()
    return Post.model_validate(response.json())
