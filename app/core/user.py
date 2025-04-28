from typing import Union
from logging import getLogger

from fastapi import Depends, Request
from fastapi_users import (
    BaseUserManager, FastAPIUsers, IntegerIDMixin, InvalidPasswordException
)
from fastapi_users.authentication import (
    AuthenticationBackend, BearerTransport, JWTStrategy
)
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.db import get_async_session
from app.models.user import User
from app.schemas.user import UserCreate

logger = getLogger(__name__)


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    """Асинхронный генератор, обеспечивает доступ к БД."""
    yield SQLAlchemyUserDatabase(session, User)


bearer_transport = BearerTransport(tokenUrl='auth/jwt/login')


# Стратегия - хранение токена в jwt
def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(
        secret=settings.secret,
        lifetime_seconds=settings.jwt_lifetime_seconds,
    )


# Объект бэкенда аутентификации
auth_backend = AuthenticationBackend(
    name='jwt', transport=bearer_transport, get_strategy=get_jwt_strategy
)


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    async def validate_password(
        self, password: str, user: Union[UserCreate, User]
    ) -> None:
        """Валидация пароля."""
        if len(password) < 3:
            raise InvalidPasswordException(
                reason='Password should be at least 3 characters'
            )
        if password.isdigit():
            raise InvalidPasswordException(
                reason='Password should not contain e-mail'
            )

    async def on_after_register(
        self, user: User, request: Union[Request, None]
    ) -> None:
        """Действие после успешной регистрации."""
        try:
            logger.info(f"Пользователь {user.email} зарегистрирован.")
        except Exception as error:
            logger.error(
                'Ошибка при регистрации пользователя',
                extra={'error': str(error)}, exc_info=True
            )


async def get_user_manager(user_db=Depends(get_user_db)):
    """Корутина, возвращающая объект класса UserManager."""
    yield UserManager(user_db)


fastapi_users = FastAPIUsers[User, int](get_user_manager, [auth_backend])

current_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)
