# itdirr

<p align="center">
  <a href="https://github.com/IRRatium/itdirr">
    <img src="assets/logo.png" width="700">
  </a>
</p>

![PyPI](https://img.shields.io/pypi/v/itdirr)
![Downloads](https://static.pepy.tech/badge/itdirr)

Расширенный форк [ITDpy](https://github.com/Gam5510/ITDpy) — Python SDK для работы с API итд.com.

> Форк сделан [IRRatium](https://github.com/IRRatium). SDK предназначен для разработки клиентских приложений и автоматизации в рамках действующих правил платформы.

## Отличия от оригинала

| Функция | ITDpy | itdirr |
|---------|-------|--------|
| Статус онлайн (`keep_online`) | ❌ | ✅ |
| Стена (`get_wall`, `post_to_wall`) | ❌ | ✅ |
| Просмотры постов (`view_post`) | ❌ | ✅ |
| Смена юзернейма (`set_username`) | ❌ | ✅ |
| Ивенты (`get_portal`) | ❌ | ✅ |
| Верификация (`get_verification_link`) | ❌ | ✅ |
| Ошибка верификации (`NotVerifiedException`) | ❌ | ✅ |
| Посты, комментарии, уведомления | ✅ | ✅ |
| Пины, опросы, настройки | ✅ | ✅ |
| Поиск, дискавери | ✅ | ✅ |

# Навигация

## Основное
- [Главная](index.md)
- [Быстрый старт](quickstart.md)

---

## Модули

- [Clans](clans.md)
- [Comments](comments.md)
- [Discovery](discovery.md)
- [Formatting](formatting.md)
- [Notifications](notifications.md)
- [Online](online.md)
- [Pins](pins.md)
- [Polls](polls.md)
- [Portal](portal.md)
- [Posts](posts.md)
- [Profile](profile.md)
- [Settings](settings.md)
- [Upload](upload.md)
- [Users](users.md)
- [Views](views.md)
- [Wall](wall.md)

---

## Модели

- [Actor](models/actor.md)
- [Comment](models/comment.md)
- [Comments](models/comments.md)
- [Discovery](models/discovery.md)
- [Notification](models/notification.md)
- [Notifications](models/notifications.md)
- [Pagination](models/pagination.md)
- [Pins](models/pins.md)
- [Poll](models/poll.md)
- [Portal](models/portal.md)
- [Post](models/post.md)
- [Posts](models/posts.md)
- [Settings](models/settings.md)
- [Users](models/users.md)

## Возможности

- Работа с постами, комментариями и опросами
- Поддержание статуса онлайн через SSE-поток
- Работа со стеной пользователей
- Управление профилем и настройками
- Поиск пользователей и хештегов
- Typed Pydantic-модели
- Строгая типизация и валидация данных
- Загрузка файлов
- HTML форматирование текста
- Информация о текущих ивентах платформы
- Автоматическая обработка ошибки верификации

## Пример использования
```python
from itdpy import ITDClient, NotVerifiedException

client = ITDClient(refresh_token="your_refresh_token")

me = client.get_me()
print(me.username)

# Текущий ивент
portal = client.get_portal()
if portal.active:
    print(f"Идёт ивент: {portal.title} — {portal.url}")

# Держать статус онлайн
client.keep_online()

# Автоматическая обработка верификации
try:
    client.create_post("Привет!")
except NotVerifiedException as e:
    print(e.verification_link)
```

## Архитектура

- Python 3.9+
- Pydantic v2
- CamelCase → snake_case
- Чистая модульная структура
