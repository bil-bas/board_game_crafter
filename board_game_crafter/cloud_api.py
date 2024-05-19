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

    def __init__(self):
        self.creds = None

        self.verify()

        # Connect to the API service
        self.service = build('drive', 'v3', credentials=self.creds)

    def verify(self) -> None:
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

    def upload(self, filepath: str, folder_id: str) -> None:
        name = os.path.basename(filepath)
        mimetype = MimeTypes().guess_type(name)[0]

        # create file metadata
        metadata = {
            'name': name,
            'mimetype': mimetype,
            'parents': [folder_id],
        }

        media = MediaFileUpload(filepath)
        files = self.service.files()

        try:
            try:
                file_id = self._get_file_id(files, name, folder_id)
            except IndexError as ex:
                result = files.create(body=metadata, media_body=media, fields='version').execute()
            else:
                metadata.pop("parents")
                result = files.update(body=metadata, media_body=media, fields='version', fileId=file_id).execute()

        except Exception as ex:
            raise RuntimeError(f"Can't Upload File: {filepath}\n{ex}")

        print(f"File Uploaded: {name} (version {result['version']})")

    def download_doc_as_pdf(self, filepath: str, folder_id: str) -> None:
        name = os.path.basename(filepath)
        fh = io.FileIO(filepath, 'wb')

        try:
            files = self.service.files()
            file_id = self._get_file_id(files, os.path.splitext(name)[0], folder_id)
            request = self.service.files().export(fileId=file_id, mimeType="application/pdf")

            downloader = MediaIoBaseDownload(fh, request, chunksize=204800)
            done = False
            while not done:
                status, done = downloader.next_chunk()
        except Exception as ex:
            raise RuntimeError(f"Can't Download File: {filepath}\n{ex}")

        print(f"File Downloaded: {name}")

    def _get_file_id(self, files, name: str, folder_id: str):
        query = f"name='{name}' and trashed=false and '{folder_id}' in parents"
        results = files.list(fields='files(id)', q=query).execute()
        file_id = results.get("files")[0]["id"]
        return file_id

