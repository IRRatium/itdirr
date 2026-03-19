from __future__ import annotations

from ..models import Post, Posts, Poll, PostUpdate
from ._common import build_query, normalize_id_list, truthy_response_status
from ..formatting import format_html

def get_posts(client, limit: int = 20, tab: str = "popular", cursor: int = 1 ) -> Posts:
    allowed_tabs = {"popular", "newest", "oldest"}

    if tab not in allowed_tabs:
        raise ValueError(
            f"Invalid sort value '{tab}'. "
            f"Allowed values: {', '.join(allowed_tabs)}"
        )
    
    query = build_query({"limit": limit, "tab": tab, "cursor": cursor})
    response = client.get(f"/api/posts?{query}")
    response.raise_for_status()
    return Posts.model_validate(response.json())


def get_post(client, post_id: str) -> Post:
    response = client.get(f"/api/posts/{post_id}")
    response.raise_for_status()
    return Post.model_validate(response.json())


def create_post(
    client,
    content: str = "",
    attachment_ids: list[str] | str | None = None,
    wall_recipient_id: str | None = None,
    poll: dict | Poll | None = None,
    parse_html: bool = False,
) -> Post:

    if parse_html:
        formatted = format_html(content)
        content = formatted["content"]
        spans = formatted["spans"]
    else:
        spans = None

    payload: dict[str, object] = {
        "content": content,
        "attachmentIds": normalize_id_list(attachment_ids),
    }

    if spans:
        payload["spans"] = spans

    if wall_recipient_id is not None:
        payload["wallRecipientId"] = wall_recipient_id

    if poll:
        if isinstance(poll, dict):
            poll = Poll.from_simple(
                question=poll["question"],
                options=poll["options"],
                multiple_choice=poll.get("multiple_choice", False),
            )

        payload["poll"] = poll.model_dump(by_alias=True)

    response = client.post("/api/posts", json=payload)
    response.raise_for_status()
    return Post.model_validate(response.json())


def update_post(client, post_id: str, content: str, parse_html: bool = False) -> dict:
    
    if parse_html:
        formatted = format_html(content)
        payload: dict[str, object] = {
            "content": formatted["content"],
            "spans": formatted["spans"]
        }
    else:
        payload: dict[str, object] = {
            "content": content
        }
    response = client.put(f"/api/posts/{post_id}", json=payload)
    response.raise_for_status()
    return PostUpdate.model_validate(response.json())


def delete_post(client, post_id: str) -> bool:
    response = client.delete(f"/api/posts/{post_id}")
    if response.status_code == 204:
        return True
    response.raise_for_status()
    return False


def like_post(client, post_id: str) -> bool:
    response = client.post(f"/api/posts/{post_id}/like")
    response.raise_for_status()
    return truthy_response_status(response.status_code)


def unlike_post(client, post_id: str) -> bool:
    response = client.delete(f"/api/posts/{post_id}/like")
    response.raise_for_status()
    return truthy_response_status(response.status_code)


def repost_post(client, post_id: str, content: str | None = None) -> bool:
    # API требует непустой content — подставляем пробел если не передан
    if content is None:
        content = " "

    payload = {"content": content}
    response = client.post(
        f"/api/posts/{post_id}/repost",
        json=payload
    )

    body = None
    try:
        body = response.json()
    except Exception:
        body = None

    response.raise_for_status()

    if isinstance(body, dict) and body.get("id"):
        return body

    return truthy_response_status(response.status_code)


def get_user_posts(client, username: str, limit: int = 20, sort: str = "new", cursor: str | None = None) -> Posts:
    if cursor:
        query = build_query({"limit": limit, "sort": sort, "cursor": cursor})
    else:
        query = build_query({"limit": limit, "sort": sort})
    
    response = client.get(f"/api/posts/user/{username}?{query}")
    response.raise_for_status()
    return Posts.model_validate(response.json())
