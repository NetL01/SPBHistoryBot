# https://console.cloud.google.com/iam-admin/serviceaccounts/details/110706065811786730814?project=kkh-tg-bot&supportedpurview=project

import httplib2
import os

from googleapiclient import discovery
from google.oauth2 import service_account

try:
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
    ]
    secret_file = os.path.join(os.getcwd(), "creds.json")

    spreadsheet_id = "1yDryv9AOPFipcJVky1TUf0pc1OhsS0iGibJRk4rOJQU/edit?usp=sharing"
    range_name = "'Рейтинг'!B9"

    credentials = service_account.Credentials.from_service_account_file(
        secret_file, scopes=scopes
    )

    service = discovery.build("sheets", "v4", credentials=credentials)


    values=service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range=range_name,
    ).execute()

    print(values.get('values'))


except OSError as e:
    print(e)