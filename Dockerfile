FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

#CMD ["alembic upgrade head", "&&", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# Команда для запуска миграций и старта приложения
CMD ["sh", "-c", "alembic upgrade head && uvicorn main:app --host 0.0.0.0 --port 8000"]
