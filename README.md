### Описание

Проект сделан на основе FastApi и python-telegram-bot

В docker-compose описаны 2 контейнера

контейнер app - API и  фоновые задач

контейнер bot - телеграм бот для админов

### Локальная разработка
использовать файл [docker-compose.local.yml](docker-compose.local.yml)


сначала запустить контейнер с БД, дождаться инициализации:

docker-compose -f docker-compose.local.yml up db

после этого можно запускать все командой:

docker-compose -f docker-compose.local.yml up -d && docker-compose logs -f

остановить контейнеры:

docker-compose -f docker-compose.local.yml down

автоматическая документаця swagger будет досутпна по 0.0.0.0:8000/peep/docs

### Деплой изменений на виртуалке

cd /home/peep_backend

git pull && docker-compose build && docker-compose down && docker-compose up -d

docker-compose logs -f

### Другое

Создать файл миграции, контейнер запущен:

docker-compose exec app bash -c "cd app && alembic revision --autogenerate -m 'change'"

Применить миграции если контейнер запущен:

docker-compose exec app bash -c "cd app && alembic upgrade head"


Применить миграции, если контейнер не запущен:

docker-compose up -d app && docker-compose exec app bash -c "cd app && alembic upgrade head" && docker-compose down

Строка подключения на mac, если бд создана локально
MYSQL_CONNECTION_STRING=mysql+mysqlconnector://peep:password@host.docker.internal:3306/peep?charset=utf8mb4
