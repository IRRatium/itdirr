from __future__ import annotations

from typing import Any
import time
import random
import requests
from requests import Response
from .auth import AuthManager
from .exceptions import NotVerifiedException
from .api import (
    create_post, 
    delete_post, 
    get_post, 
    get_posts, 
    get_user_posts, 
    like_post, 
    repost_post, 
    unlike_post, 
    update_post, 
    create_comment, 
    delete_comment, 
    get_comments,
    like_comment,
    reply_to_comment,
    unlike_comment,
    follow_user,
    get_followers,
    get_following,
    get_me,
    get_user,
    unfollow_user,
    get_notifications,
    mark_all_notification_read,
    mark_notification_read,
    get_top_clans,
    upload_file,
    update_profile,
    get_replies,
    get_pins,
    set_pin, 
    remove_pin,
    vote,
    who_to_follow,
    search_hashtags,
    search,
    update_notification_settings,
    update_privacy,
    get_trending_hashtags,
    keep_online,
    get_wall,
    post_to_wall,
    view_post,
    view_posts,
    get_portal,
    download_banner,
)
from .models import *

class ClientInitResult:
    def __init__(self, client=None, error=None):
        self.client = client
        self.error = error
        self.success = client is not None

    def __bool__(self):
        return self.success

class ITDClient:
    ######################################################
    ############  Низкоуровневые методы API ##############
    ######################################################
    
    _DEFAULT_TIMEOUT = 15
    _UPLOAD_TIMEOUT = 3600
    _SDK_NAME = "itdpy"
    _SDK_VERSION = "0.7.1"
    _PLATFORM = "python"

    def __init__(self, refresh_token: str, auto_auth: bool = True, enable_retry: bool = True):
        self.base_url = "https://xn--d1ah4a.com"
        self.session = requests.Session()

        self._auth_failed: bool = False
        self._enable_retry = enable_retry
        self._access_token: str | None = None
        self._user_id: str | None = None
        self._auth_manager: Any = None

        self.session.headers.update(
            {
                "Origin": self.base_url,
                "Referer": f"{self.base_url}/",
            }
        )

        self.session.cookies.set(
            name="refresh_token",
            value=refresh_token,
            domain="xn--d1ah4a.com",
            path="/api",
        )

        self._apply_user_agent(initial=True)
        if auto_auth:
            auth = AuthManager(self)
            self._bind_auth_manager(auth)

            try:
                refreshed = auth.refresh_access_token()
                if not refreshed:
                    self._auth_failed = True
            except Exception:
                self._auth_failed = True
                print("⚠ Invalid refresh token")

    @property
    def access_token(self) -> str | None:
        return self._access_token

    @property
    def user_id(self) -> str | None:
        return self._user_id
    
    @property
    def is_authenticated(self) -> bool:
        return not self._auth_failed

    def _bind_auth_manager(self, auth_manager: Any) -> None:
        self._auth_manager = auth_manager

    def _set_access_token(self, token: str) -> None: 
        self._access_token = token 
        self.session.headers["Authorization"] = f"Bearer {token}"

    def _set_user_id(self, user_id: str) -> None:
        self._user_id = user_id
        self._apply_user_agent()

    def _build_user_agent(self, initial: bool = False) -> str:
        if initial or not self._user_id:
            return (
                f"{self._SDK_NAME}/{self._SDK_VERSION} "
                f"(initial; platform={self._PLATFORM})"
            )
        return (
            f"{self._SDK_NAME}/{self._SDK_VERSION} "
            f"(userid={self._user_id}; platform={self._PLATFORM})"
        )

    def _apply_user_agent(self, initial: bool = False) -> None:
        self.session.headers["User-Agent"] = self._build_user_agent(initial)

    def _request(
        self,
        method: str,
        path: str,
        *,
        retry: bool = True,
        retry_count: int = 0,
        **kwargs
    ):
        if not path.startswith("/"):
            path = f"/{path}"

        url = f"{self.base_url}{path}"
        timeout = kwargs.pop("timeout", (5, 10))

        try:
            response = self.session.request(method, url, timeout=timeout, **kwargs)
        except requests.RequestException:
            fake = requests.Response()
            fake.status_code = 0
            fake._content = b"Network error"
            return fake

        # Проверка верификации телефона
        if response.status_code == 403:
            try:
                body = response.json()
                error = body.get("error", {})
                if error.get("code") == "PHONE_VERIFICATION_REQUIRED":
                    raise NotVerifiedException(self._user_id)
            except NotVerifiedException:
                raise
            except Exception:
                pass

        if response.status_code == 401 and retry and self._auth_manager and "/auth/refresh" not in path:
            refreshed = self._auth_manager.refresh_access_token()
            if refreshed:
                return self._request(method, path, retry=False, **kwargs)

        if response.status_code == 429 and self._enable_retry:
            if retry_count >= 3:
                print("⚠ Rate limit max retries reached.")
                return response

            wait_time = random.uniform(1.5, 3.5)
            print(f"⚠ Rate limited. Sleeping {wait_time:.2f}s")
            time.sleep(wait_time)

            return self._request(
                method,
                path,
                retry=retry,
                retry_count=retry_count + 1,
                **kwargs
            )

        return response

    def get(self, path: str, **kwargs: Any) -> Response:
        return self._request("GET", path, **kwargs)

    def post(self, path: str, **kwargs: Any) -> Response:
        return self._request("POST", path, **kwargs)

    def put(self, path: str, **kwargs: Any) -> Response:
        return self._request("PUT", path, **kwargs)

    def patch(self, path: str, **kwargs: Any) -> Response:
        return self._request("PATCH", path, **kwargs)

    def delete(self, path: str, **kwargs: Any) -> Response:
        return self._request("DELETE", path, **kwargs)
    
    @classmethod
    def create(cls, refresh_token: str):
        client = cls(refresh_token, auto_auth=False, enable_retry=False)

        auth = AuthManager(client)
        client._bind_auth_manager(auth)

        try:
            refreshed = auth.refresh_access_token()
        except Exception as e:
            return ClientInitResult(
                client=None,
                error={
                    "type": "auth_exception",
                    "message": str(e),
                }
            )

        if not refreshed:
            return ClientInitResult(
                client=None,
                error={
                    "type": "invalid_token",
                    "message": "Invalid refresh token",
                }
            )

        response = client.get("/api/users/me")

        if response.status_code != 200:
            return ClientInitResult(
                client=None,
                error={
                    "type": "auth_failed",
                    "status_code": response.status_code,
                    "message": response.text or "Authentication failed",
                }
            )

        return ClientInitResult(client=client)

    ######################################################
    ############  Высокоуровневые методы API #############
    ######################################################

    def create_comment(
        self,
        post_id: str,
        content: str,
        attachment_ids: list[str] | str | None = None,
    ) -> Comment:
        return create_comment(self, post_id, content, attachment_ids)

    def reply_to_comment(
        self,
        comment_id: str,
        content: str,
        attachment_ids: list[str] | str | None = None,
    ) -> Comment:
        return reply_to_comment(self, comment_id, content, attachment_ids)
    
    def delete_comment(self, comment_id: str) -> bool:
        return delete_comment(self, comment_id)
    
    def like_comment(self, comment_id: str) -> bool:
        return like_comment(self, comment_id)
    
    def unlike_comment(self, comment_id: str) -> bool:
        return unlike_comment(self, comment_id)

    def get_comments(self, post_id: str, limit: int = 20, sort: str = "popular") -> Comments:
        return get_comments(self, post_id, limit, sort)
    
    def upload_file(self, file_path):
        return upload_file(self, file_path)
    
    def get_top_clans(self):
        return get_top_clans(self)
    
    def get_notifications(self, offset: int = 0, limit: int = 20) -> Notifications:
        return get_notifications(self, offset, limit)
    
    def mark_notification_read(self, notification_id) -> bool:
        return mark_notification_read(self, notification_id)
    
    def mark_all_notification_read(self, notification_ids=None):
        return mark_all_notification_read(self, notification_ids)
    
    def get_posts(self, limit: int = 20, tab: str = "popular", cursor: int = 1) -> Posts:
        return get_posts(self, limit, tab, cursor)
    
    def get_post(self, post_id: str) -> Post:
        return get_post(self, post_id)
    
    def create_post(
        self,
        content: str = "",
        attachment_ids: list[str] | str | None = None,
        wall_recipient_id: str | None = None,
        poll: dict | Poll | None = None,
        parse_html: bool = False,
    ) -> Post:
        return create_post(self, content, attachment_ids, wall_recipient_id, poll, parse_html)
    
    def update_post(self, post_id: str, content: str, parse_html: bool = False) -> dict:
        return update_post(self, post_id, content, parse_html)
    
    def delete_post(self, post_id: str) -> bool:
        return delete_post(self, post_id)
    
    def like_post(self, post_id: str) -> bool:
        return like_post(self, post_id)
    
    def unlike_post(self, post_id: str) -> bool:
        return unlike_post(self, post_id)
    
    def repost_post(self, post_id: str, content: str | None = None) -> bool:
        return repost_post(self, post_id, content)
    
    def get_user_posts(self, username: str, limit: int = 20, sort: str = "new", cursor: str | None = None) -> Posts:
        return get_user_posts(self, username, limit, sort, cursor)
    
    def update_profile(
        self,
        *,
        display_name: str | None = None,
        username: str | None = None,
        bio: str | None = None,
        banner_id: str | None = None,
    ) -> Me:
        return update_profile(self, display_name=display_name, username=username, bio=bio, banner_id=banner_id)
    
    def get_me(self) -> Me:
        return get_me(self)
    
    def get_user(self, username: str) -> User:
        return get_user(self, username)
    
    def follow_user(self, username: str) -> bool:
        return follow_user(self, username)
    
    def unfollow_user(self, username: str) -> bool:
        return unfollow_user(self, username)
    
    def get_followers(self, username: str, page: int = 1, limit: int = 30) -> Users:
        return get_followers(self, username, page, limit)
    
    def get_following(self, username: str, page: int = 1, limit: int = 30) -> Users:
        return get_following(self, username, page, limit)

    def get_replies(self, comment_id: str, sort="newest"):
        return get_replies(self, comment_id, sort)
    
    def get_pins(self):
        return get_pins(self)
    
    def remove_pin(self):
        return remove_pin(self)
    
    def set_pin(self, slug):
        return set_pin(self, slug)
    
    def vote(self, post_id, option_ids):
        return vote(self, post_id, option_ids)
    
    def who_to_follow(self):
        return who_to_follow(self)
    
    def search_hashtags(self, name, limit=20):
        return search_hashtags(self, name, limit)
    
    def search(self, query, user_limit=5, hashtag_limit=5):
        return search(self, query, user_limit, hashtag_limit)
    
    def update_privacy(
        self,
        *,
        is_private: bool | None = None,
        wall_access: str | None = None,
        likes_visibility: str | None = None,
        show_last_seen: bool | None = None,
    ):
        return update_privacy(
            self,
            is_private=is_private,
            wall_access=wall_access,
            likes_visibility=likes_visibility,
            show_last_seen=show_last_seen,
        )

    def update_notification_settings(
        self,
        *,
        enabled: bool | None = None,
        comments: bool | None = None,
        follows: bool | None = None,
        likes: bool | None = None,
        mentions: bool | None = None,
        sound: bool | None = None,
        wall_posts: bool | None = None,
    ):
        return update_notification_settings(
            self,
            enabled=enabled,
            comments=comments,
            follows=follows,
            likes=likes,
            mentions=mentions,
            sound=sound,
            wall_posts=wall_posts,
        )
    
    def get_trending_hashtags(self, limit: int = 10):
        return get_trending_hashtags(self, limit)

    # --- Методы IRRatium ---

    def keep_online(self, on_event=None, background: bool = True):
        """
        Поддерживает статус "в сети" через SSE-поток.

        Параметры:
            on_event   — колбэк(event_type, data) для уведомлений в реальном времени
            background — True (по умолчанию): запускает в фоновом потоке

        Пример:
            client.keep_online()

            def handler(event, data):
                if event == "like":
                    print("Новый лайк!")
            client.keep_online(on_event=handler)
        """
        return keep_online(self, on_event=on_event, background=background)

    def get_wall(self, username: str, limit: int = 20, cursor: str | None = None):
        """Получить посты со стены пользователя."""
        return get_wall(self, username, limit, cursor)

    def post_to_wall(self, username: str, content: str):
        """Написать пост на стену пользователя."""
        return post_to_wall(self, username, content)

    def view_post(self, post_id: str) -> bool:
        """Отметить пост как просмотренный."""
        return view_post(self, post_id)

    def view_posts(self, post_ids: list[str]) -> dict[str, bool]:
        """Отметить несколько постов как просмотренные."""
        return view_posts(self, post_ids)

    def set_username(self, username: str) -> Me:
        """
        Сменить юзернейм текущего пользователя.

        Пример:
            client.set_username("mynewname42")
        """
        return self.update_profile(username=username)

    def get_portal(self) -> Portal:
        """
        Получить информацию о текущем ивенте на платформе.

        Пример:
            portal = client.get_portal()
            if portal.active:
                print(f"Идёт ивент: {portal.title}")
                print(f"Ссылка: {portal.url}")
        """
        return get_portal(self)

    def get_verification_link(self) -> str:
        """
        Получить ссылку для верификации аккаунта через Telegram.

        Пример:
            link = client.get_verification_link()
            print("Верифицируй аккаунт:", link)
        """
        user_id = self._user_id or self.get_me().id
        return f"https://t.me/itd_verification_bot?start={user_id}"
    
    
    def download_banner(self, username: str, path: str) -> str | None:
    """
    Скачать баннер пользователя и сохранить в файл.
    Возвращает путь к файлу или None если баннера нет.

    Пример:
        client.download_banner("gam5510", "banner.png")
        client.download_banner("gam5510", "banner.gif")
    """
    from .api.banner import download_banner
    return download_banner(self, username, path)
