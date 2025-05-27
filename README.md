# Library API

RESTful API для управления библиотечным каталогом, разработанное на FastAPI с использованием PostgreSQL, SQLAlchemy, Alembic и JWT-аутентификации.

## Требования

- Python 3.8+ (рекомендуется 3.11 или 3.13)
- Git
- (В будущем) PostgreSQL

## Установка

1. Клонируйте репозиторий:
   ```bash
   git clone <URL_репозитория>
   cd pyTraineeLibraryTask
   ```

2. Создайте и активируйте виртуальное окружение:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Linux/Mac
   ```

3. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

## Запуск

### Вариант 1: Через `fastapi dev` (рекомендуемый)
```bash
fastapi dev src/main.py
```

### Вариант 2: Через `uvicorn`
```bash
uvicorn src.main:app --reload
```

### Вариант 3: Через `make` (опционально)
Создайте `Makefile`:
```makefile
dev:
    fastapi dev src/main.py

dev-uvicorn:
    uvicorn src.main:app --reload
```
Запустите:
```bash
make dev
```

Сервер доступен на:
- `http://127.0.0.1:8000`
- `http://127.0.0.1:8000/docs`

## Структура проекта
```
pyTraineeLibraryTask/
├── src/
│   ├── __init__.py
│   └── main.py
├── requirements.txt
├── README.md
```

## Текущий прогресс
- Настроена базовая структура.
- Установлены FastAPI и Uvicorn.
- Реализован тестовый эндпоинт (`GET /`).

## Следующие шаги
- Настройка PostgreSQL и SQLAlchemy.
- Создание моделей и миграций с Alembic.