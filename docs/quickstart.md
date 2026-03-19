# itdirr

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

## Быстрый старт

![Получение токена](https://i.ibb.co/DH1m8GL7/Assistant.png)

1. Открой итд.com в браузере и войди в аккаунт
2. Открой DevTools (F12) → Application → Cookies
3. Найди куку `refresh_token` и скопируй значение

```python
from itdpy import ITDClient

client = ITDClient(refresh_token="ваш_refresh_token")

me = client.get_me()
print(me.id)
print(me.username)
print(me.followers_count)
```

---

## Примеры

### Обновление имени в реальном времени

```python
from itdpy import ITDClient
from datetime import datetime
import time

client = ITDClient(refresh_token="ваш_токен")

while True:
    client.update_profile(display_name=f"Имя |{datetime.now().strftime('%m.%d %H:%M:%S')}|")
    time.sleep(1)
```

### Обновление баннера

```python
from itdpy import ITDClient

client = ITDClient(refresh_token="ваш_токен")

file = client.upload_file("banner.gif")
update = client.update_profile(banner_id=file.id)
print(update.banner)
```

### Держать статус онлайн

```python
from itdpy import ITDClient

client = ITDClient(refresh_token="ваш_токен")

client.keep_online()

import time
while True:
    time.sleep(1)
```

### Обработка уведомлений в реальном времени

```python
from itdpy import ITDClient

client = ITDClient(refresh_token="ваш_токен")

def on_event(event_type, data):
    if event_type == "like":
        print("Новый лайк!")
    elif event_type == "comment":
        print("Новый комментарий!")
    elif event_type == "follow":
        print("Новый подписчик!")

client.keep_online(on_event=on_event)
```

### Проверить текущий ивент

```python
from itdpy import ITDClient

client = ITDClient(refresh_token="ваш_токен")

portal = client.get_portal()
if portal.active:
    print(f"Идёт ивент: {portal.title}")
    print(f"Ссылка: {portal.url}")
```

### Верификация аккаунта

```python
from itdpy import ITDClient, NotVerifiedException

client = ITDClient(refresh_token="ваш_токен")

# Получить ссылку вручную
link = client.get_verification_link()
print("Верифицируй аккаунт:", link)

# Или поймать автоматически при любом действии
try:
    client.create_post("Привет!")
except NotVerifiedException as e:
    print(e.verification_link)
```

← [Назад к документации](index.md)
