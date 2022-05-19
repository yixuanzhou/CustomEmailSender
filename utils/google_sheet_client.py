from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
SHEET_ID = os.environ['SHEET_ID']


class GoogleSheetClient:

    def __init__(self):
        creds = None
        if os.path.exists('static/credentials/token.pickle'):
            with open('static/credentials/token.pickle', 'rb') as token:
                creds = pickle.load(token)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'static/credentials/credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            with open('static/credentials/token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        self.service = build('sheets', 'v4', credentials=creds)

    def read_sheet(self, sheet_name):
        sheet = self.service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SHEET_ID, range=sheet_name, valueRenderOption='FORMATTED_VALUE').execute()
        values = result.get('values', [])
        data = []

        if not values:
            print('No data found.')
        else:
            for value in values:  # skip the table header
                data.append([value[0]])
                # data.append(dict(zip(values[0][:-1], value)))
        print(*data, sep="\n")  # print each element in new line
        return data

    def get_sheet_list(self):
        resp = self.service.spreadsheets().get(spreadsheetId=SHEET_ID).execute()
        sheets = resp["sheets"]
        sheet_names = []
        for sheet in sheets:
            sheet_names.append(sheet['properties']['title'])
        print(sheet_names)
        return sheet_names


if __name__ == "__main__":
    # pass
    gsc = GoogleSheetClient()
    gsc.read_sheet("GRAYMAIL")
    gsc.get_sheet_list()