import os
import json
import requests
from dotenv import load_dotenv
from datetime import datetime, timedelta
from urllib.parse import quote

load_dotenv()

ODOO_URL = os.getenv("ODOO_URL")
ODOO_DB = os.getenv("ODOO_DB")
ODOO_USERNAME = os.getenv("ODOO_USERNAME")
ODOO_PASSWORD = os.getenv("ODOO_PASSWORD")

REPORT_TYPE = "koontor_weekly"
COMPANY_ID = 1

today = datetime.today()
from_date = today - timedelta(days=30)

FROM_DATE = from_date.strftime("%Y-%m-%d")
TO_DATE = today.strftime("%Y-%m-%d")

session = requests.Session()


def login():
    payload = {
        "jsonrpc": "2.0",
        "method": "call",
        "params": {
            "db": ODOO_DB,
            "login": ODOO_USERNAME,
            "password": ODOO_PASSWORD
        },
        "id": 1
    }

    response = session.post(
        f"{ODOO_URL}/web/session/authenticate",
        json=payload
    )

    response.raise_for_status()

    data = response.json()

    if "error" in data:
        raise Exception(json.dumps(data["error"], indent=4))

    uid = data["result"]["uid"]

    print("Login Successful")
    print("UID :", uid)
    
    print(session.cookies.get_dict())
    print("CSRF :", session.cookies.get("csrf_token"))

    return uid


def create_wizard(uid):

    payload = {
        "jsonrpc": "2.0",
        "method": "call",
        "params": {
            "model": "brand.sales.wizard",
            "method": "web_save",
            "args": [
                [],
                {
                    "report_type": REPORT_TYPE,
                    "company_id": COMPANY_ID,
                    "date_from": FROM_DATE,
                    "date_to": TO_DATE
                },
                {
                    "report_type": {},
                    "company_id": {},
                    "date_from": {},
                    "date_to": {}
                }
            ],
            "kwargs": {
                "context": {
                    "lang": "en_US",
                    "tz": "Asia/Dhaka",
                    "uid": uid,
                    "allowed_company_ids": [COMPANY_ID]
                }
            }
        },
        "id": 2
    }

    response = session.post(
        f"{ODOO_URL}/web/dataset/call_kw/brand.sales.wizard/web_save",
        json=payload
    )

    response.raise_for_status()

    result = response.json()

    print("=" * 100)
    print(json.dumps(result, indent=4))
    print("=" * 100)

    if "error" in result:
        raise Exception(json.dumps(result["error"], indent=4))

    wizard_id = result["result"][0]["id"]

    print("Wizard ID :", wizard_id)

    return wizard_id


def generate_report(uid, wizard_id):

    payload = {
        "jsonrpc": "2.0",
        "method": "call",
        "params": {
            "model": "brand.sales.wizard",
            "method": "action_generate_xlsx_report",
            "args": [[wizard_id]],
            "kwargs": {
                "context": {
                    "lang": "en_US",
                    "tz": "Asia/Dhaka",
                    "uid": uid,
                    "allowed_company_ids": [COMPANY_ID],
                    "active_model": "brand.sales.wizard",
                    "active_id": wizard_id,
                    "active_ids": [wizard_id]
                }
            }
        },
        "id": 3
    }

    response = session.post(
        f"{ODOO_URL}/web/dataset/call_kw/brand.sales.wizard/action_generate_xlsx_report",
        json=payload
    )

    response.raise_for_status()

    result = response.json()

    if "error" in result:
        raise Exception(json.dumps(result["error"], indent=4))

    report = result["result"]

    print(json.dumps(report, indent=4))

    return report


def download_report(report):

    options = json.dumps(report["data"], separators=(",", ":"))
    context = json.dumps(report["context"], separators=(",", ":"))

    report_url = (
        f"{ODOO_URL}/report/xlsx/{report['report_name']}"
        f"?options={quote(options)}"
        f"&context={quote(context)}"
    )

    response = session.get(report_url)

    print("Download Status :", response.status_code)

    if response.status_code != 200:
        raise Exception(response.text)

    # sanity check - make sure it's actually an xlsx, not an HTML error page
    content_type = response.headers.get("Content-Type", "")
    if "html" in content_type.lower():
        raise Exception("Got HTML instead of xlsx:\n" + response.text[:500])

    filename = f"{REPORT_TYPE}.xlsx"

    with open(filename, "wb") as file:
        file.write(response.content)

    print("=" * 100)
    print("Excel Saved Successfully")
    print(filename)
    print("=" * 100)

    return filename

   


if __name__ == "__main__":

    uid = login()

    wizard_id = create_wizard(uid)

    report = generate_report(uid, wizard_id)

    excel_file = download_report(report)

    print("Done :", excel_file)