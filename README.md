
Применить миграции, если контейнер не запущен

docker-compose up -d && docker-compose exec app bash -c "cd app && alembic upgrade head" && docker-compose down

Применить миграции если контейнер запущен

docker-compose exec app bash -c "cd app && alembic upgrade head"