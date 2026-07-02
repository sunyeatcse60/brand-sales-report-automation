# import gspread
# import pandas as pd
# from gspread_dataframe import set_with_dataframe
# from google.oauth2.service_account import Credentials

# SCOPES = [
#     "https://www.googleapis.com/auth/spreadsheets",
#     "https://www.googleapis.com/auth/drive"
# ]

# creds = Credentials.from_service_account_file(
#     "gcreds.json",
#     scopes=SCOPES
# )

# client = gspread.authorize(creds)

# SHEET_ID = "1hIbIXX-pMWvJ7dhugxm89RxfcmRweCghnwb0veE_NWg"

# spreadsheet = client.open_by_key(SHEET_ID)

# worksheet = spreadsheet.sheet1

# df = pd.read_excel("koontor_weekly.xlsx")

# worksheet.clear()

# set_with_dataframe(worksheet, df)

# print("Google Sheet Updated Successfully")





import gspread
import pandas as pd
from gspread_dataframe import set_with_dataframe
from google.oauth2.service_account import Credentials

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

SHEET_ID = "1hIbIXX-pMWvJ7dhugxm89RxfcmRweCghnwb0veE_NWg"


def upload_excel_to_sheet(excel_file):
    creds = Credentials.from_service_account_file(
        "gcreds.json",
        scopes=SCOPES
    )

    client = gspread.authorize(creds)

    spreadsheet = client.open_by_key(SHEET_ID)

    worksheet = spreadsheet.sheet1

    df = pd.read_excel(excel_file)

    worksheet.clear()

    set_with_dataframe(worksheet, df)

    print("Google Sheet Updated Successfully")