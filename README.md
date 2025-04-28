# Cat Charity Fund API

## Описание

API для управления благотворительным фондом помощи котикам. Позволяет создавать благотворительные проекты, делать пожертвования и управлять пользователями.

## Технологии

*   **Python**: Основной язык программирования.
*   **FastAPI**: Фреймворк для создания API.
*   **SQLAlchemy**: ORM для работы с базами данных.
*   **Async SQLAlchemy**: Асинхронная работа с базами данных.
*   **SQLite**: База данных (может быть заменена на PostgreSQL или другую).
*   **Pydantic**: Для валидации данных.
*   **FastAPI Users**: Для управления пользователями и аутентификацией.

## Установка

1.  Клонируйте репозиторий:

    ```
    git clone git@github.com:Lasellar/cat_charity_fund.git
    cd cat_charity_fund
    ```
2.  Создайте и активируйте виртуальное окружение:

    ```
    python3 -m venv venv
    source venv/bin/activate # или venv\Scripts\activate в Windows
    ```
3.  Установите зависимости:

    ```
    pip install -r requirements.txt
    ```
    *Важно!* 
    Для корректной работы необходим Python < 3.11

## Настройка

1.  Создайте файл `.env` в корне проекта и заполните его переменными окружения:

    ```
    APP_TITLE="Cat Charity Fund"
    APP_DESCRIPTION="API for managing a cat charity fund"
    DATABASE_URL="sqlite+aiosqlite:///./cat_charity_fund.db"
    SECRET="YOUR_SECRET_KEY"
    JWT_LIFETIME_SECONDS=3600
    ```

    Замените `YOUR_SECRET_KEY` на ваш секретный ключ.
2.  Примените миграции:

    ```
    alembic upgrade head
    ```

## Запуск

1.  Запустите сервер:

    ```
    uvicorn app.main:app --reload
    ```

    API будет доступен по адресу [http://127.0.0.1:8000](http://127.0.0.1:8000).

## API endpoints

### Charity Projects

*   `POST /charity_project/`: Создать проект (только для суперпользователей).
*   `GET /charity_project/`: Получить все проекты.
*   `DELETE /charity_project/{project_id}`: Удалить проект (только для суперпользователей).
*   `PATCH /charity_project/{project_id}`: Обновить проект (только для суперпользователей).

### Donations

*   `GET /donation/`: Получить все пожертвования (только для суперпользователей).
*   `POST /donation/`: Создать новое пожертвование.
*   `GET /donation/my`: Получить пожертвования текущего пользователя.

### Users

*   `/auth/jwt/login`: Авторизация.
*   `/auth/register`: Регистрация.
*   `/users`: Управление пользователями (только для суперпользователей).

## Дополнительно

*   Для работы с API рекомендуется использовать [Swagger UI](http://localhost:8000/docs) или [ReDoc](http://localhost:8000/redoc).
*   Для аутентификации используйте JWT токены.
*   Удаление пользователей запрещено, используйте деактивацию.