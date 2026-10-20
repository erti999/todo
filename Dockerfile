FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код
COPY alembic.ini .
COPY migrations/ ./migrations/
COPY app/ ./app/

# Создаем непривилегированного пользователя
RUN useradd -m -u 1000 fastapi && chown -R fastapi:fastapi /app
USER fastapi

# Порт приложения
EXPOSE 8000

# Запуск приложения
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]