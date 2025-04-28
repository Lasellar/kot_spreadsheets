from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models import CharityProject
from app.schemas.charity_project import CharityProjectUpdate


async def check_name_duplicate(
        project_name: str, session: AsyncSession
) -> None:
    """Проверяет, что имя проекта уникально."""
    project_id = await charity_project_crud.get_project_id_by_name(
        project_name, session
    )
    if project_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Проект с таким именем уже существует!",
        )


async def check_charity_project_exists(
    project_id: int, session: AsyncSession
) -> CharityProject:
    """Проверяет существование проекта по ID и возвращает его."""
    charity_project = await charity_project_crud.get(project_id, session)
    if charity_project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Проект не найден!"
        )
    return charity_project


async def check_charity_project_closed_or_invested(project: CharityProject):
    """Проверяет, что проект не закрыт и в него не внесены средства."""
    if project.close_date is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="В проект были внесены средства, не подлежит удалению!",
        )

    if project.invested_amount > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="В проект были внесены средства, не подлежит удалению!",
        )


async def check_charity_project_fully_invested(project: CharityProject):
    """Проверяет, что проект не закрыт."""
    if project.fully_invested:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Закрытый проект нельзя редактировать!",
        )


async def check_full_amount_not_less_than_invested(
    project: CharityProject, obj_in: CharityProjectUpdate
) -> None:
    """Проверяет, что новая сумма не меньше уже вложенной."""
    if obj_in.full_amount is not None and (
            obj_in.full_amount < project.invested_amount
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Нельзя установить требуемую сумму меньше уже вложенной.",
        )
