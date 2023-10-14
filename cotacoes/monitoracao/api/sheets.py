from google.oauth2 import service_account
from googleapiclient.discovery import build

class Spreadsheet:
    spreadsheet_id = '1uypMIKinfs1VS8p2U6y-zzQqqnrPfPkc6V-WTOc1CyI'

    def __init__(self):
        credentials = service_account.Credentials.from_service_account_file("creds.json", scopes=["https://www.googleapis.com/auth/spreadsheets"])
        service = build("sheets", "v4", credentials=credentials)
        self._values = service.spreadsheets().values()
                
    def find_row(self, asset):
        result = self._values.get(spreadsheetId=Spreadsheet.spreadsheet_id, range='A:A').execute()
        values = result.get('values')
        row = values.index([asset])+1
        return row
    
    def get_price(self, row):
        result = self._values.get(spreadsheetId=Spreadsheet.spreadsheet_id, range=f'B{row}:B{row}').execute()
        value = result.get('values')[0][0]
        return value