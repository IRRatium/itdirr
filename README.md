# ITDpy

<p align="center">
  <img src="https://i.postimg.cc/gJ9z8RDk/ITDpy-(1)-pixian-ai.png" width="700">
</p>

![PyPI version](https://img.shields.io/pypi/v/itdpy)
![Downloads](https://static.pepy.tech/badge/itdpy)
![License](https://img.shields.io/github/license/Gam5510/ITDpy)

Python SDK для социальной сети итд.com.
> ⚠️ Неофициальный API-клиент.  
>SDK предназначен для разработки клиентских приложений и тестирования API в рамках действующих правил платформы.

## Установка pip
```bash
pip install itdpy
```

### Через git

```bash
git clone https://github.com/Gam5510/ITDpy
cd itdpy
pip install -r requirements.txt
pip install -e .
```

## Документация  

[![Docs](https://img.shields.io/badge/docs-online-blue)](https://gam5510.github.io/ITDpy/)


## Быстрый старт

> Blockquote ![Получение токена](https://i.ibb.co/DH1m8GL7/Assistant.png)
Как получить токен

```python
from  itdpy.client  import  ITDClient

client  =  ITDClient(refresh_token="Ваш refresh token")

me  =  client.get_me()
print(me.id)
print(me.username)
```

### Скрипт на обновление имени

```python
from  itdpy.client  import  ITDClient
from  datetime  import  datetime
import  time

client = ITDClient(refresh_token="Ваш_токен")

while  True:
	client.update_profile(display_name=f"Фазлиддин |{datetime.now().strftime('%m.%d %H:%M:%S')}|")
	time.sleep(1)
```

### Скрипт на обновление баннера 
```python
from  itdpy.client  import  ITDClient

client  =  ITDClient(refresh_token="Ваш_токен")

file  =  client.upload_file(client,  "matrix-rain-effect-animation-photoshop-editor.gif")
print(file.id)
update  =  update_profile(client,  banner_id=file.id)
print(update.banner)
```

# Костомные запросы  

## ✅ Базовый пример кастомного GET
```python
response = client.get("/api/users/me")
data = response.json() 
print(data)
```
### Можно добавить любой эндпоинт
----------

## ✅ POST с JSON
```python
response = client.post( 
		"/api/posts",
    json={ "content": "Привет из кастомного запроса" }
) 
print(response.status_code) 
print(response.json())
```
----------

## ✅ PUT / PATCH
```python
response = client.patch( "/api/profile",
    json={ "displayName": "Фазлиддин 😎" }
)
```
----------

## ✅ DELETE
```python
client.delete("/api/posts/POST_ID") 
```
----------

## ✅ Передача query-параметров
```python
response = client.get( "/api/posts",
    params={ "limit": 50, "sort": "popular" }
)
```

## Планы

- Асинхронная версия библиотеки (`aioitd`)
- Улучшенная обработка и форматирование ошибок
- Логирование (через `logging`)
- Расширение объектной модели (Post, Comment, User и др.)
- Дополнительные API-эндпоинты по мере появления
- Улучшение документации и примеров


## Прочее

Проект активно развивается.
Если у вас есть идеи или предложения — создавайте issue или pull request.