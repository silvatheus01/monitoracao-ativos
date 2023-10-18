from google.oauth2 import service_account
from googleapiclient.discovery import build
import pathlib
from datetime import datetime

SPREADSHEET_ID = '1uypMIKinfs1VS8p2U6y-zzQqqnrPfPkc6V-WTOc1CyI'
ASSET_COLUMN = 'A'
PRICE_COLUMN = 'B'
TRADETIME_COLUMN = 'C'

class Security:
    def __init__(self, price, tradetime):
        self.price = price
        self.tradetime = tradetime

class Spreadsheet:
    def __init__(self):
        path = pathlib.Path(__file__).resolve().parent
        credentials = service_account.Credentials.from_service_account_file(f'{path}/creds.json', scopes=["https://www.googleapis.com/auth/spreadsheets"])
        service = build("sheets", "v4", credentials=credentials)
        self._values = service.spreadsheets().values()

    def find_row(self, asset_name):
        result = self._values.get(spreadsheetId=SPREADSHEET_ID, range=f'{ASSET_COLUMN}:{ASSET_COLUMN}').execute()
        values = result.get('values')
        row = values.index([asset_name])+1  
        return row
    
    def get_security(self, row):
        result = self._values.get(spreadsheetId=SPREADSHEET_ID, range=f'{PRICE_COLUMN}{row}:{TRADETIME_COLUMN}{row}').execute()
        values = result.get('values')[0]
        
        price = float(values[0].replace(',','.'))
        tradetime = values[1]
        format = "%d/%m/%Y %H:%M:%S"  
        data_obj = datetime.strptime(tradetime, format)

        return Security(price, data_obj)