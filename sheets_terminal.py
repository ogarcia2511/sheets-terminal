from __future__ import print_function
import pickle
import os.path
import sys
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = '1ZkCDJt1--JiKUOFMo3AbL9j0X8EazyHVmaD9nWLStZY'
RANGE_NAME = 'list!A3'

def auth_API():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials = creds)

    return service

def read_API():
    # Authenticate and call the Sheets API
    service = auth_API()
    
    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId = SPREADSHEET_ID,
                                range = RANGE_NAME).execute()
    values = result.get('values', [])

    if not values: 
        print('No data found.')
    else:
        print("\n - - - - SPREADSHEET - - - -")
        for row in values:
            for item in row:
                print('%s' % item, end = '\t')
            print('\n')

def write_API():
    # Authenticate
    service = auth_API()

    # Set up editing request
    values = [
        [
            # Cell values ...
            5
        ],
        # Additional rows ...
    ]
    value_input_option = "USER_ENTERED"
    body = { 'values': values }
    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().update(spreadsheetId = SPREADSHEET_ID,
                                range = RANGE_NAME, 
                                valueInputOption = value_input_option,
                                body = body).execute()
    values = result.get('values', [])
    

    return

def write_args():
    print("What cells to operate on? Use Google A1 format.")
    cell_range = input()

    RANGE_NAME.append("!" + cell_count)
    # maybe write try-catch in write_API()
    # to report back if range invalid ??

    print("What values to enter in?")
    values = input()

    write_API(values, cell_range)

def parse_a1_notation():
    return

def main(argv):
    read = write = False;

    for cmd in argv[1:]:
        if cmd == '-r' or cmd == '--read':    
            read = True
        elif cmd == '-w' or cmd == '--write':
            write = True
        else:
            print("Wrong args! Use -r/--read or -w/--write as args.")
            return

    if read == write:
        print("Args error! Use one of -r/--read or -w/--write.")
        return

    if read:
        read_API()
        return
    elif write:
      #   write_args()
        write_API()
        return

if __name__ == "__main__":
    main(sys.argv)
