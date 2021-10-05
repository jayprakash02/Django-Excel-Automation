import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from apiclient import errors

# define the scope
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive',
         'https://www.googleapis.com/auth/drive.metadata.readonly']

# add credentials to the account
creds = ServiceAccountCredentials.from_json_keyfile_name(
    '/home/jay/Downloads/Freelance/project_Sameer_US/backend/service-gcp-key.json', scope)

# authorize the clientsheet
client = gspread.authorize(creds)
service_excel = build('sheets', 'v4', credentials=creds)
service_drive = build('drive', 'v2', credentials=creds)


class SpreadsheetSnippets(object):
    def __init__(self, service_excel,service_drive):
        self.service_excel = service_excel
        self.service_drive = service_drive


    def create(self, title):
        service = self.service_excel
        # [START sheets_create]
        spreadsheet = {
            'properties': {
                'title': title
            }
        }
        spreadsheet = service.spreadsheets().create(body=spreadsheet,
                                                    fields='spreadsheetId').execute()
        print('Spreadsheet ID: {0}'.format(spreadsheet.get('spreadsheetId')))
        # [END sheets_create]
        self.insert_permission(spreadsheet.get('spreadsheetId'),['unijay12@gmail.com'],'user','writer')
        return spreadsheet.get('spreadsheetId')

    def listFiles(self):
        service=self.service_drive
        results = service.files().list(
            pageSize=10, fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])

        if not items:
            print('No files found.')
        else:
            print('Files:')
            for item in items:
                print(item)

    def insert_permission(self,file_id, value, perm_type, role):
        service = self.service_drive
        """Insert a new permission.

        Args:
            service: Drive API service instance.
            file_id: ID of the file to insert permission for.
            value: User or group e-mail address, domain name or None for 'default'
                type.
            perm_type: The value 'user', 'group', 'domain' or 'default'.
            role: The value 'owner', 'writer' or 'reader'.
        Returns:
            The inserted permission if successful, None otherwise.
        """
        new_permission = {
            'value': value,
            'type': perm_type,
            'role': role
        }
        try:
            return service.permissions().insert(
                fileId=file_id, body=new_permission).execute()
        except errors.HttpError as error:
            print('An error occurred: %s' % error)
        return None


# SpreadsheetSnippets(service).create('hello')
SpreadsheetSnippets(service_excel,service_drive).create('check1')
