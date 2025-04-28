from datetime import datetime
from typing import Optional

from pydantic import BaseModel, PositiveInt

from app.schemas.base import AbstractBaseSchema


class DonationBase(BaseModel):
    """Базовая схема пожертвования."""
    comment: Optional[str]
    full_amount: PositiveInt


class DonationDBUser(DonationBase):
    """Схема пожертвования для возврата из БД для обычного юзера."""
    id: int
    comment: Optional[str]
    create_date: datetime

    class Config:
        orm_mode = True


class DonationDBAdmin(DonationDBUser, AbstractBaseSchema):
    """Схема пожертвования для возврата из БД для суперюзера."""
    user_id: int
