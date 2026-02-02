import gspread
from google.oauth2.service_account import Credentials
from config import SPREADSHEET_NAME, GOOGLE_CREDENTIALS_JSON, worksheet_names, NEW_STATE
import json
import os
from dotenv import load_dotenv
load_dotenv() 

def authenticate_google_sheets():
    creds = json.loads(os.environ["GOOGLE_CREDENTIALS_JSON"])
    scope = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]
    credentials = Credentials.from_service_account_info(creds, scopes=scope)
    
    """Аутентифікація та створення клієнта Google Sheets"""
    client = gspread.authorize(credentials)
    return client

def fetch_sheet_data(client, worksheet_name):
    """Отримати дані з Google Sheets"""
    spreadsheet = client.open(SPREADSHEET_NAME)
    worksheet = spreadsheet.worksheet(worksheet_name)
    data = worksheet.get_all_values()
    if not data:
        return [], "", []
    res = []

    keys = data[0]
    rows = data[1:]

    for row in rows:
        if not row:
            continue

        status = row[0].strip().lower()
        if status != NEW_STATE.lower():
            continue
        row += [""] * (len(keys) - len(row))

        res.append(dict(zip(keys, row)))

    return res, worksheet, keys


