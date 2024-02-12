import os

import gspread_asyncio
from dotenv import load_dotenv
from google.oauth2.service_account import Credentials

load_dotenv()

SCOPES = [os.environ.get('SCOPES')]
SPREADSHEET_ID = os.environ.get('SPREADSHEET_ID')


def get_creds():
    """Получение данных для Google сервиса"""
    creds = Credentials.from_service_account_file(
        'src/tasks/google_api_config/creds.json', scopes=SCOPES
    )

    return creds


agcm = gspread_asyncio.AsyncioGspreadClientManager(get_creds)


async def get_spreadsheet():
    """Получение google таблицы"""
    agc = await agcm.authorize()
    spreadsheet = await agc.open_by_key(SPREADSHEET_ID)
    return await spreadsheet.get_sheet1()


async def get_sheet_values() -> list[list]:
    """Получение данных с google таблицы"""
    sheet = await get_spreadsheet()
    values = await sheet.get_all_values()

    return values
