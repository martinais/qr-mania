import os.path
from datetime import date
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets',
          'https://www.googleapis.com/auth/userinfo.profile']

# The ID and range of a sample spreadsheet
SAMPLE_SPREADSHEET_ID = '1VzZQVC9d68j9YyXwDK3_7GC1OedZPV9HTW6PbXgzGxU'  # TODO to parmetrize
lineNumber = '9'
SAMPLE_RANGE_NAME = 'Library!G' + lineNumber + ':I' + lineNumber  # TODO improve the way to write in a specific area


def connect():
    """Shows basic usage of the Sheets API.
        Prints values from a sample spreadsheet.
        """

    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())


def getUserInfo(creds):
    try:
        service = build('people', 'v1', credentials=creds)

        # Call the People API
        print('List 10 connection names')
        results = service.people().get(
            resourceName='people/me',
            personFields='names,emailAddresses'
        ).execute()
        connections = results.get('names', [])
        print(connections)

        return connections[0].get('displayName')
        for person in connections:
            names = person.get('names', [])
            if names:
                name = names[0].get('displayName')
                print(name)
    except HttpError as err:
        print(err)


def editSheetInfo(creds, user, range):
    try:
        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range=range).execute()
        values = result.get('values', [])

        if not values:
            print('No data found.')
            return

        """for row in values:
            # Print columns A and E, which correspond to indices 0 and 4.
            print(row[0])"""

        # Write data

        if (values[0][0] == 'Disponible'):
            data = 'Emprumté'
            retrieveDate = date.today().strftime("%d/%m/%Y")

        else:
            data = 'Disponible'
            retrieveDate = ''
            user = ''
        response = sheet.values().update(
            spreadsheetId=SAMPLE_SPREADSHEET_ID,
            range=range,
            valueInputOption='RAW',
            body={"values":
                [
                    [data, user, retrieveDate]
                ]
            }
        ).execute()
        return response

    except HttpError as err:
        print(err)


def main():
    creds = connect()
    getUserInfo(creds)
    editSheetInfo(creds)


if __name__ == '__main__':
    main()
