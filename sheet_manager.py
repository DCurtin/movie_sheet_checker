"""
    This file contains the class for managing sheets, primarily used for 
    movie manager but can be repurposed for any doc that wishes to pull a
    sheet or range of elements form a sheet.
"""
from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

class SheetManager(object):
    """
        This class will manage reading and writing to a google doc sheet
    """
    sheet_id = None
    service = None
    last_sheet = None
    needs_update = False

    # If modifying these scopes, delete your previously saved credentials
    # at ~/.credentials/sheets.googleapis.com-python-quickstart.json
    SCOPES = 'https://www.googleapis.com/auth/spreadsheets' #read and write
    CLIENT_SECRET_FILE = 'client_secret.json'
    APPLICATION_NAME = 'Google Sheets API Python Quickstart'

    def __init__(self, sheet_id):
        """
            Initialize the MovieManager with a sheet ID so the manager will know
            what sheet to read from and write to
        """
        self.sheet_id = sheet_id
        credentials = self.get_credentials()
        http = credentials.authorize(httplib2.Http())
        discovery_url = ('https://sheets.googleapis.com/$discovery/rest?'\
                'version=v4')
        self.service = discovery.build('sheets', 'v4', http=http,
                discoveryServiceUrl=discovery_url)

    def get_sheet(self, force_update=False, sheet_name='Sheet1'):
        """
            retrieve the sheet from the class, if the sheet has been
            unchanged it will not query it from google
        """

        range_name = sheet_name
        """
            range_name would define a range of cells to grab
            by handing the sheet_name you ask for the entire sheet
        """

        if self.service == None:
            print("SheetManager was not propperly initialized")
            return None

        if self.needs_update is True:
            force_update = True
            self.needs_update = False

        if force_update is True or self.last_sheet is None:
            results = self.service.spreadsheets().values().get(
                    spreadsheetId=self.sheet_id,
                    range=range_name).execute()
            last_sheet = results.get('values', [])
            #get sheet from google

        return last_sheet

    def update_sheet(self, updated_sheet, sheet_name='Sheet1'):
        """
            This function will take a sheet and sheet name, over
            writing the old sheet or range of elements provided with
            the sheet name.
        """
        #take list and write it over
        #I think I'll write over the entire sheet

        range_name = sheet_name
        updated_sheet_body = {'values' : updated_sheet}
        self.service.spreadsheets().values().update(
                          spreadsheetId=self.sheet_id, range=range_name,
                          valueInputOption='USER_ENTERED',
                          body=updated_sheet_body).execute()

        self.needs_update = True

    def get_credentials(self):
        """Gets valid user credentials from storage.

        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.

        Returns:
            Credentials, the obtained credential.
        """
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')

        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)

        credential_path = os.path.join(credential_dir,
            'sheets.googleapis.com-python-quickstart.json')

        store = Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            """
                if credentials have not been set or are invalid they must be
                reset this should be done in a manual run of the script and
                not left to cron
            """
            flow = client.flow_from_clientsecrets(self.CLIENT_SECRET_FILE,
                    self.SCOPES)
            """
                start the procedure for initializing credentials
            """

            flow.user_agent = self.APPLICATION_NAME

            credentials = tools.run(flow, store)
            print('Storing credentials to ' + credential_path)
        return credentials
