from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive',
         'https://www.googleapis.com/auth/drive.metadata.readonly']

# add credentials to the account
creds = ServiceAccountCredentials.from_json_keyfile_name('service-gcp-key.json', scope)