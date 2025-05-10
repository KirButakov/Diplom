#!/bin/sh

# Ждём, пока контейнер с базой данных запустится
echo "Waiting for DB to start..."
sleep 10  # Задержка в 10 секунд

# Ожидание доступности базы данных
until nc -z db 5432; do
  echo "Waiting for DB..."
  sleep 1
done

echo "DB is ready! Starting Django..."

# Запуск Django
exec python manage.py runserver 0.0.0.0:8000