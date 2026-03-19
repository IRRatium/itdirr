# itdirr

<p align="center">
  <img src="https://i.ibb.co/MxbWvPh9/itdirr.png" width="700">
</p>

<p align="center">
  <a href="https://pypi.org/project/itdirr/"><img src="https://img.shields.io/pypi/v/itdirr?color=blue&label=PyPI" alt="PyPI"></a>
  <a href="https://pepy.tech/project/itdirr"><img src="https://static.pepy.tech/badge/itdirr" alt="Downloads"></a>
  <a href="https://github.com/Gam5510/ITDpy/blob/main/LICENSE"><img src="https://img.shields.io/github/license/Gam5510/ITDpy" alt="License"></a>
  <img src="https://img.shields.io/badge/python-3.9+-blue" alt="Python 3.9+">
</p>

<p align="center">
  Расширенный форк <a href="https://github.com/Gam5510/ITDpy">ITDpy</a> — неофициальный Python SDK для <a href="https://итд.com">итд.com</a>
</p>

> Форк сделан [IRRatium](https://github.com/IRRatium).  
> Неофициальный API-клиент. SDK предназначен для разработки приложений и автоматизации в рамках правил платформы.

---

## Отличия от оригинала

| Функция | ITDpy | itdirr |
|---------|-------|-----------|
| Статус онлайн (`keep_online`) | ❌ | ✅ |
| Стена (`get_wall`, `post_to_wall`) | ❌ | ✅ |
| Просмотры постов (`view_post`) | ❌ | ✅ |
| Смена юзернейма (`set_username`) | ❌ | ✅ |
| Посты, комментарии, уведомления | ✅ | ✅ |
| Пины, опросы, настройки | ✅ | ✅ |
| Поиск, дискавери | ✅ | ✅ |

---

## Установка

```bash
pip install itdirr
```

Или через git:
```bash
git clone https://github.com/IRRatium/itdirr
cd itdirr
pip install -e .
```

---

## Быстрый старт

```python
from itdpy import ITDClient

client = ITDClient(refresh_token="ваш_токен")

me = client.get_me()
print(me.username)
print(me.display_name)
print(me.followers_count)
```

<details>
<summary>Как получить refresh_token</summary>

1. Открой итд.com в браузере и войди в аккаунт
2. Открой DevTools (F12) → Application → Cookies
3. Найди куку `refresh_token` и скопируй значение

</details>

---

## Возможности

### Пользователи
```python
me = client.get_me()

user = client.get_user("gam5510")
print(user.bio, user.followers_count, user.online)

client.follow_user("gam5510")
client.unfollow_user("gam5510")

followers = client.get_followers("gam5510", page=1, limit=30)
following = client.get_following("gam5510")
```

### Профиль
```python
client.update_profile(display_name="Новое имя", bio="Описание")

# Быстрая смена юзернейма
client.set_username("coolname42")

# Загрузить баннер
file = client.upload_file("banner.gif")
client.update_profile(banner_id=file.id)
```

### Посты
```python
posts = client.get_posts(limit=20, tab="popular")  # popular / newest / oldest

post = client.create_post("Привет!")

# С HTML-форматированием
post = client.create_post("<b>Жирный</b> и <i>курсив</i>", parse_html=True)

# С опросом
post = client.create_post(
    content="Голосуем!",
    poll={"question": "Лучший язык?", "options": ["Python", "Go", "Rust"]}
)

# С медиафайлом
file = client.upload_file("photo.jpg")
post = client.create_post("Фото!", attachment_ids=[file.id])

client.like_post(post.id)
client.unlike_post(post.id)
client.repost_post(post.id, content="Мой комментарий")
client.view_post(post.id)
client.delete_post(post.id)

posts = client.get_user_posts("gam5510")
```

### Комментарии
```python
comments = client.get_comments(post_id, limit=20, sort="popular")

comment = client.create_comment(post_id, "Отличный пост!")
client.reply_to_comment(comment.id, "Согласен!")
client.like_comment(comment.id)
client.delete_comment(comment.id)

replies = client.get_replies(comment.id)
```

### Стена ✨
```python
wall = client.get_wall("gam5510")
client.post_to_wall("gam5510", "Привет!")
```

### Статус онлайн ✨
```python
# Держать онлайн в фоне — одна строка
client.keep_online()

# С обработкой событий в реальном времени
def on_event(event_type, data):
    if event_type == "like":
        print("Новый лайк!")
    elif event_type == "comment":
        print("Новый комментарий!")
    elif event_type == "follow":
        print("Новый подписчик!")

client.keep_online(on_event=on_event)

# Блокирующий режим
client.keep_online(background=False)
```

### Уведомления
```python
notifications = client.get_notifications(limit=20)
for n in notifications:
    print(n.type, n.actor.username)

client.mark_notification_read(notification_id)
client.mark_all_notification_read([id1, id2])
```

### Пины
```python
pins = client.get_pins()
client.set_pin(slug="kirill67_202602_infected")
client.remove_pin()
```

### Настройки
```python
client.update_privacy(
    is_private=True,
    wall_access="followers",   # everyone / followers / mutual / nobody
    likes_visibility="mutual",
    show_last_seen=False,
)

client.update_notification_settings(
    likes=True,
    comments=True,
    sound=False,
)
```

### Поиск и дискавери
```python
results = client.search("python")
posts = client.search_hashtags("python")
trends = client.get_trending_hashtags(limit=10)
suggestions = client.who_to_follow()
```

### Опросы
```python
post = client.get_post(post_id)
client.vote(post.id, option_ids=post.poll.options[0].id)
```

---

## Кастомные запросы

```python
response = client.get("/api/users/me")
data = response.json()

response = client.post("/api/posts", json={"content": "Привет!"})

client.put("/api/users/me", json={"displayName": "Новое имя"})
client.delete("/api/posts/POST_ID")

response = client.get("/api/posts", params={"limit": 50, "sort": "popular"})
```

---

## Модели

| Модель | Описание |
|--------|----------|
| `Me` | Текущий пользователь |
| `User` | Профиль пользователя |
| `UserLite` | Краткий профиль (в постах, комментариях) |
| `Post` | Пост |
| `Posts` | Список постов с пагинацией |
| `Comment` | Комментарий |
| `Notification` | Уведомление |
| `Poll` / `PollOption` | Опрос |
| `Pin` / `Pins` | Пины профиля |
| `Attachment` | Медиафайл |
| `PrivacySettings` | Настройки приватности |
| `NotificationSettings` | Настройки уведомлений |

Все модели на **Pydantic v2**, автоматический маппинг `camelCase → snake_case`.

---

## Документация оригинала

[![Docs](https://img.shields.io/badge/docs-ITDpy-blue)](https://gam5510.github.io/ITDpy/)

---

## Планы

- [ ] Async-клиент (`asyncio`)
- [ ] Логирование через `logging`
- [ ] Новые эндпоинты по мере появления

---

## Благодарности

Оригинальная библиотека — [ITDpy](https://github.com/Gam5510/ITDpy) by [Gam5510](https://github.com/Gam5510)

---

## Лицензия

MIT © [IRRatium](https://github.com/IRRatium)
