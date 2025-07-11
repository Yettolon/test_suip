# Suip Parser API

Проект для парсинга метаданных файлов через сайт suip.biz с помощью Playwright и сохранением результатов в базу PostgreSQL.

---

## Быстрый старт

### 1. Создайте файл `.env`
Скопируйте пример и настройте переменные окружения под себя:

```bash
cp .env.example .env
```

### 2. Запустите сервисы через Docker Compose:
```bash
docker compose up --build
```

### 3. Откройте Swagger:
`http://127.0.0.1:8000/docs`


## Особенности
- **Временные файлы**: Загружаемые файлы сохраняются во временной папке `/tmp` внутри контейнера.
- **Конфигурация**: Все параметры (например, `DATABASE_URL`) задаются в файле `.env`. Убедитесь, что файл создан и заполнен корректно.
- **База данных**: При изменении моделей базы данных необходимо пересоздать таблицы. (Сделано без миграций)
- **Запуск**:
  - **Через Docker**: Используйте `docker compose up --build` для запуска.
  - **Локально**: Требуется Python 3.11+ и установка зависимостей из `requirements.txt` (`pip install -r requirements.txt`).
- **Контроль качества кода**: Настроен `pre-commit` с линтерами и проверкой типов (`mypy`, `flake8`, `black`).
