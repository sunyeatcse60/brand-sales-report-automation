import gspread
import pandas as pd
from gspread_dataframe import set_with_dataframe
from google.oauth2.service_account import Credentials
from datetime import datetime
from zoneinfo import ZoneInfo

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

    # Read Excel
    df = pd.read_excel(excel_file)

    # Clear previous data
    worksheet.clear()

    # Upload dataframe starting from A5
    set_with_dataframe(
        worksheet,
        df,
        row=5,
        col=1,
        include_index=False,
        include_column_header=True,
        resize=True
    )

    # Current Date (Bangladesh Time)
    today = datetime.now(
        ZoneInfo("Asia/Dhaka")
    ).strftime("%b-%y")        # Example: Jul-26

    # Date in middle
    worksheet.update("J2", [[today]])

    # Format the date cell
    worksheet.format(
        "J2",
        {
            "backgroundColor": {
                "red": 0.85,
                "green": 0.95,
                "blue": 0.85
            },
            "textFormat": {
                "bold": True,
                "fontSize": 14
            },
            "horizontalAlignment": "CENTER"
        }
    )

    print(f"{sheet_name} Updated Successfully")