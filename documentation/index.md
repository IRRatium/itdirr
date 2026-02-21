# ITDpy

Python SDK для работы с API итд.com.

>SDK предназначен для разработки клиентских приложений и тестирования API в рамках действующих правил платформы.

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
- [Pins](pins.md) 
- [Polls](polls.md)  
- [Posts](posts.md) 
- [Profile](profile.md) 
- [Settings](settings.md)
- [Upload](upload.md)
- [Users](users.md)   
  
  
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
- [Post](models/post.md)  
- [Posts](models/posts.md)  
- [Settings](models/settings.md)
- [Users](models/users.md)  

## Назначение

ITDpy предоставляет удобную Python-обёртку над API итд.com и позволяет:

-   интегрировать функциональность сайта в собственные приложения
-   разрабатывать пользовательские интерфейсы
-   создавать экспериментальные и учебные проекты
-   расширять функциональность платформы в рамках API
    
SDK не модифицирует поведение сервера и использует только официальные API-эндпоинты.

## Возможности

-   Работа с постами, комментариями и опросами
-   Получение статистики 
-   Управление профилем и настройками
-   Поиск пользователей и хештегов
-   Typed Pydantic-модели
-   Строгая типизация и валидация данных
-   Загружать файлы 
-   HTML форматирование текста

## Пример использования
```python
from  itdpy  import  ITDClient  
  
client  =  ITDClient(refresh_token="your_refresh_token")  

me  =  client.get_me()  
print(me.username)
```
## Архитектура

-   Python 3.11+
-   Pydantic v2
-   CamelCase → snake_case
-   Чистая модульная структура

