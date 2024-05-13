# https://www.geeksforgeeks.org/upload-and-download-files-from-google-drive-storage-using-python/?ref=ml_lbp
import pickle
import os.path
import io
import shutil
from mimetypes import MimeTypes

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload


class DriveAPI:
    # Define the scopes
    SCOPES = ['https://www.googleapis.com/auth/drive']
    PICKLE_FILE = '/home/bil/.google-drive-token.pickle'
    CREDENTIALS_FILE = '/home/bil/.google-drive-credentials.json'
    FOLDER_ID = '1zP7Kwvm6AoIVuCKzXB7zGUuNZbkMDOl6'

    def __init__(self):
        self.creds = None

        self.verify()

        # Connect to the API service
        self.service = build('drive', 'v3', credentials=self.creds)

        # request a list of first N files or
        # folders with name and id from the API.
        # resource = self.service.files()
        # results = resource.list(pageSize=100, fields="files(id, name)").execute()
        # items = results.get('files')
        # print(*items, sep="\n", end="\n\n")

    def verify(self):
        # Check if file token.pickle exists
        if os.path.exists(self.PICKLE_FILE):
            # Read the token from the file and
            # store it in the variable self.creds
            with open(self.PICKLE_FILE, 'rb') as token:
                self.creds = pickle.load(token)
        # If no valid credentials are available,
        # request the user to log in.
        if not self.creds or not self.creds.valid:
            # If token is expired, it will be refreshed,
            # else, we will request a new one.
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(self.CREDENTIALS_FILE, self.SCOPES)
                self.creds = flow.run_local_server(port=0)

            # Save the access token in token.pickle
            # file for future usage
            with open(self.PICKLE_FILE, 'wb') as token:
                pickle.dump(self.creds, token)

    def upload(self, filepath):
        # Extract the file name out of the file path
        name = os.path.basename(filepath)

        # Find the MimeType of the file
        mimetype = MimeTypes().guess_type(name)[0]

        # create file metadata
        metadata = {
            'name': name,
            'mimetype': mimetype,
        }

        try:
            media = MediaFileUpload(filepath, mimetype=mimetype)
            files = self.service.files()
            results = files.list(fields='files(id)', q=f"name='{name}' and trashed=false").execute()
            file_id = results.get("files")[0]["id"]
            result = files.update(body=metadata, media_body=media, fields='version', fileId=file_id).execute()
            print(f"File Uploaded: {os.path.basename(filepath)} (version {result['version']})")
        except Exception as ex:
            raise RuntimeError(f"Can't Upload File: {ex}")
