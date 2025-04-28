from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    """Схема с базовыми полями юзера."""
    pass


class UserCreate(schemas.BaseUserCreate):
    """
    Схема для создания пользователя.
    Обязательные поля: email, password.
    """
    pass


class UserUpdate(schemas.BaseUserUpdate):
    """
    Схема для обновления объекта пользователя.
    Все поля опциональные.
    """
