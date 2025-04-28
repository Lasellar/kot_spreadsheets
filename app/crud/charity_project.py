from typing import Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject


class CRUDCharityProject(CRUDBase):
    async def get_project_id_by_name(
        self, project_name: str, session: AsyncSession,
    ) -> Union[int, None]:
        """Получить проект по названию."""
        db_project_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == project_name
            )
        )
        db_project_id = db_project_id.scalars().first()
        return db_project_id

    async def get_projects_by_completion_rate(self, session: AsyncSession):
        """Получить список закрытых проектов."""
        projects = await session.execute(
            select(
                CharityProject.name,
                CharityProject.close_date,
                CharityProject.create_date,
                CharityProject.description
            ).where(
                CharityProject.close_date.isnot(None)
            ).order_by(
                (CharityProject.close_date - CharityProject.create_date).asc()
            )
        )
        projects = projects.all()
        result = [
            {
                'name': name,
                'close_date': close_date,
                'create_date': create_date,
                'description': description
            }
            for name, close_date, create_date, description in projects
        ]
        return result


charity_project_crud = CRUDCharityProject(CharityProject)
