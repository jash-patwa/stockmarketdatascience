"""
Google Drive handler for accessing vehicle data files.
Handles authentication and file download/upload.
"""

import os
import pickle
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.api_python_client import discovery
from typing import Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GoogleDriveHandlerError(Exception):
    """Base exception for Google Drive handler."""
    pass


class GoogleDriveHandler:
    """Handles Google Drive operations for vehicle data files."""

    SCOPES = ['https://www.googleapis.com/auth/drive']

    def __init__(self, credentials_path: str = 'credentials.json',
                 token_path: str = 'token.pickle'):
        """
        Initialize Google Drive handler.

        Args:
            credentials_path: Path to OAuth credentials JSON file
            token_path: Path to save/load OAuth token
        """
        self.credentials_path = credentials_path
        self.token_path = token_path
        self.service = None
        self._authenticate()

    def _authenticate(self) -> None:
        """Authenticate with Google Drive using OAuth."""
        try:
            creds = None

            # Load token if it exists
            if os.path.exists(self.token_path):
                with open(self.token_path, 'rb') as token_file:
                    creds = pickle.load(token_file)

            # Refresh or create new credentials
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            elif not creds or not creds.valid:
                if os.path.exists(self.credentials_path):
                    flow = InstalledAppFlow.from_client_secrets_file(
                        self.credentials_path, self.SCOPES)
                    creds = flow.run_local_server(port=0)
                else:
                    raise GoogleDriveHandlerError(
                        f"Credentials file not found at {self.credentials_path}")

            # Save the token for future use
            with open(self.token_path, 'wb') as token_file:
                pickle.dump(creds, token_file)

            # Build the service
            self.service = discovery.build('drive', 'v3', credentials=creds)
            logger.info("Successfully authenticated with Google Drive")

        except Exception as e:
            logger.error(f"Authentication error: {e}")
            raise GoogleDriveHandlerError(f"Failed to authenticate: {str(e)}")

    def find_file_by_name(self, filename: str) -> Optional[str]:
        """
        Find a file by name in Google Drive.

        Args:
            filename: Name of the file to find

        Returns:
            File ID if found, None otherwise
        """
        try:
            query = f"name='{filename}' and trashed=false"
            results = self.service.files().list(
                q=query,
                spaces='drive',
                fields='files(id, name)',
                pageSize=10
            ).execute()

            files = results.get('files', [])
            if files:
                logger.info(f"Found file: {files[0]['name']} (ID: {files[0]['id']})")
                return files[0]['id']
            else:
                logger.warning(f"File not found: {filename}")
                return None

        except Exception as e:
            logger.error(f"Error finding file: {e}")
            return None

    def download_file(self, file_id: str, output_path: str) -> bool:
        """
        Download a file from Google Drive.

        Args:
            file_id: Google Drive file ID
            output_path: Local path to save the file

        Returns:
            True if successful, False otherwise
        """
        try:
            request = self.service.files().get_media(fileId=file_id)
            with open(output_path, 'wb') as file:
                file.write(request.execute())

            logger.info(f"Downloaded file to {output_path}")
            return True

        except Exception as e:
            logger.error(f"Error downloading file: {e}")
            return False

    def upload_file(self, file_path: str, file_name: str,
                   parent_id: Optional[str] = None) -> Optional[str]:
        """
        Upload a file to Google Drive.

        Args:
            file_path: Local path to the file
            file_name: Name for the file in Google Drive
            parent_id: Optional parent folder ID

        Returns:
            File ID if successful, None otherwise
        """
        try:
            file_metadata = {'name': file_name}
            if parent_id:
                file_metadata['parents'] = [parent_id]

            media = discovery.MediaFileUpload(file_path, resumable=True)
            file_result = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id'
            ).execute()

            file_id = file_result.get('id')
            logger.info(f"Uploaded file {file_name} (ID: {file_id})")
            return file_id

        except Exception as e:
            logger.error(f"Error uploading file: {e}")
            return None

    def update_file(self, file_id: str, file_path: str) -> bool:
        """
        Update an existing file on Google Drive.

        Args:
            file_id: Google Drive file ID
            file_path: Local path to the updated file

        Returns:
            True if successful, False otherwise
        """
        try:
            media = discovery.MediaFileUpload(file_path, resumable=True)
            self.service.files().update(
                fileId=file_id,
                media_body=media
            ).execute()

            logger.info(f"Updated file (ID: {file_id})")
            return True

        except Exception as e:
            logger.error(f"Error updating file: {e}")
            return False
