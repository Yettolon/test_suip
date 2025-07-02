FROM python:3.11-slim

WORKDIR /app

# Установка зависимостей
COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Установка Playwright и браузеров
RUN playwright install --with-deps

# Только теперь копируем исходники
COPY ./src ./src

# Запуск
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
