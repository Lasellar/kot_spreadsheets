from datetime import datetime

from aiogoogle import Aiogoogle

from app.core.config import settings
from app.models import CharityProject

FORMAT = '%Y/%m/%d %H:%M:%S'
FORMAT_FOR_SHEETS = '%d days, %H:%M:%S'


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')
    spreadsheet_body = {
        'properties': {'title': f'Отчёт на {now_date_time}',
                       'locale': 'ru_RU'},
        'sheets': [{'properties': {'sheetType': 'GRID',
                                   'sheetId': 0,
                                   'title': 'Лист 1',
                                   'gridProperties': {'rowCount': 100,
                                                      'columnCount': 100}}}]
    }
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    spreadsheetid = response.get('spreadsheetId')
    return spreadsheetid


async def set_user_permissions(
        spreadsheetid: str,
        wrapper_services: Aiogoogle
) -> None:
    permissions_body = {'type': 'user',
                        'role': 'writer',
                        'emailAddress': settings.email_user}
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheetid, json=permissions_body, fields='id'
        )
    )


async def spreadsheets_update_value(
        spreadsheetid: str,
        charity_projects: list[CharityProject],
        wrapper_services: Aiogoogle
) -> None:
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')
    table_values = [
        ['Отчет от', now_date_time],
        ['Топ проектов по скорости закрытия'],
        ['Название проекта', 'Время сбора', 'Описание']
    ]
    for project in charity_projects:
        delta = project.get('close_date') - project.get('create_date')
        days = delta.days
        seconds = delta.seconds
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        formatted_duration = f"{days} days {hours:02}:{minutes:02}:{seconds}"
        new_row = [
            project.get('name'),
            formatted_duration,
            project.get('description')
        ]
        table_values.append(new_row)
    update_body = {'majorDimension': 'ROWS', 'values': table_values}
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheetid,
            range='A1:C100',
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )
