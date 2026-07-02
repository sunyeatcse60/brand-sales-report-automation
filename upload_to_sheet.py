import gspread
import pandas as pd
from gspread_dataframe import set_with_dataframe
from google.oauth2.service_account import Credentials

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

SHEET_ID = "1hIbIXX-pMWvJ7dhugxm89RxfcmRweCghnwb0veE_NWg"


def upload_excel_to_sheet(excel_file, sheet_name):

    creds = Credentials.from_service_account_file(
        "gcreds.json",
        scopes=SCOPES
    )

    client = gspread.authorize(creds)

    spreadsheet = client.open_by_key(SHEET_ID)

    try:
        worksheet = spreadsheet.worksheet(sheet_name)
    except gspread.WorksheetNotFound:
        worksheet = spreadsheet.add_worksheet(
            title=sheet_name,
            rows=100,
            cols=50
        )

    df = pd.read_excel(excel_file)

    worksheet.clear()

    set_with_dataframe(
        worksheet,
        df,
        include_index=False,
        include_column_header=True,
        resize=True
    )

    print(f"{sheet_name} Updated Successfully")