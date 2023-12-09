#  Foodgram

## Описание

**Foodgram** - это веб-приложение, созданное с использованием Django, которое предоставляет пользователям возможность делиться рецептами любимых блюд.

## Установка и запуск
Склонируйте репозиторий на ваш сервер: 
 
``` 
https://github.com/NRenat/foodgram.git
```

Запустить Docker контейнер
```
sudo docker compose -f docker-compose.production.yml down
sudo docker compose -f docker-compose.production.yml up -d
sudo docker compose -f docker-compose.production.yml exec backend python manage.py migrate
sudo docker compose -f docker-compose.production.yml exec backend python manage.py collectstatic
sudo docker compose -f docker-compose.production.yml exec backend cp -r /app/collected_static/. /static/static/
```


## Админка:

```
- email: qq@qq.qq
- password: qq
```

## Адрес проекта:

```
- http://158.160.27.119:8000/
```
