# !/usr/bin/env python
# @Date    : 2022-05-18
# @Author  : Yixuan Zhou (ethanzhou@alumni.usc.edu)
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
    """GoogleSheetClient is used to read Google Sheet data using googleapis"""
    def __init__(self):
        """Client Constructor"""
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
        """Function to read data in Google Sheet with SHEET_ID

        :param string sheet_name: sheet name
        :return list
        """
        sheet = self.service.spreadsheets()  # pylint: disable=maybe-no-member
        result = sheet.values().get(spreadsheetId=SHEET_ID, range=sheet_name,
                                    valueRenderOption='FORMATTED_VALUE').execute()
        values = result.get('values', [])
        return values

    def get_sheet_list(self):
        """Function to get all sheet names in Google Sheet with SHEET_ID

        :return list: Sheet Names
        """
        resp = self.service.spreadsheets().get(spreadsheetId=SHEET_ID).execute()  # pylint: disable=maybe-no-member
        sheets = resp["sheets"]
        sheet_names = []
        for sheet in sheets:
            sheet_names.append(sheet['properties']['title'])
        return sheet_names
