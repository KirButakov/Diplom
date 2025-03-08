FROM python:3.9-slim

# Устанавливаем netcat-openbsd и шрифт DejaVu
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        netcat-openbsd \
        fonts-dejavu && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Сборка статических файлов
RUN python manage.py collectstatic --noinput

# Скрипт для ожидания базы данных
COPY wait-for-db.sh /wait-for-db.sh
RUN chmod +x /wait-for-db.sh
