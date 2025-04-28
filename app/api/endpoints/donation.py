from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.models import User
from app.schemas.donation import (
    DonationDBAdmin, DonationBase, DonationDBUser
)
from app.services.investment import invest_funds

router = APIRouter()


@router.get(
    "/",
    response_model_exclude_none=True,
    response_model=list[DonationDBAdmin],
    dependencies=[Depends(current_superuser)],
)
async def get_all_donation(
        session: AsyncSession = Depends(get_async_session)
):
    """Получить все пожертвования (только для суперюзеров)."""
    return await donation_crud.get_multi(session)


@router.post(
    "/",
    response_model_exclude_none=True,
    response_model=DonationDBUser,
)
async def create_donation(
    donation: DonationBase,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    """Создать новое пожертвование и инвестировать средства."""
    new_donation = await donation_crud.create(donation, session, user)
    new_donation = await invest_funds(new_donation, session)
    return new_donation


@router.get("/my", response_model=list[DonationDBUser])
async def get_user_donations(
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Получить пожертвования текущего пользователя."""
    return await donation_crud.get_user_donations(user, session)
