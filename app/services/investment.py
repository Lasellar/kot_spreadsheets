from datetime import datetime
from typing import Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.charity_project import CharityProject
from app.models.donation import Donation


def mark_as_invested(db_obj):
    """
    Помечает объект как полностью инвестированный.
    Устанавливает флаг fully_invested в True и задаёт
    текущую дату в поле close_date.
    """
    db_obj.fully_invested = True
    db_obj.close_date = datetime.now()


async def invest_funds(
    obj_in: Union[CharityProject, Donation], session: AsyncSession
):
    """
    Инвестирует средства между объектами CharityProject и Donation.
    Функция распределяет доступные средства из obj_in между активными
    объектами противоположного типа (если obj_in — Donation, то
    распределяет по CharityProject и наоборот), обновляет суммы
    инвестиций и помечает объекты как полностью инвестированные
    при достижении полной суммы.
    """
    db_model = CharityProject if isinstance(obj_in, Donation) else Donation

    active_objs = await session.execute(
        select(db_model)
        .where(db_model.fully_invested.is_(False))
        .order_by(db_model.create_date.asc(), db_model.id.asc())
    )
    active_objs = active_objs.scalars().all()

    for active_obj in active_objs:
        required = obj_in.full_amount - obj_in.invested_amount
        if required <= 0:
            break

        available = active_obj.full_amount - active_obj.invested_amount
        transfer = min(required, available)

        obj_in.invested_amount += transfer
        active_obj.invested_amount += transfer

        if active_obj.invested_amount == active_obj.full_amount:
            mark_as_invested(active_obj)
        if obj_in.invested_amount == obj_in.full_amount:
            mark_as_invested(obj_in)

        session.add(active_obj)

    session.add(obj_in)
    await session.commit()
    await session.refresh(obj_in)
    return obj_in
