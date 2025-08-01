"""Gmail service for sending emails."""
import os.path
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from helpers import paths_helper

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

# Configuration files
CONFIG_DIR = os.path.join(os.path.dirname(__file__), "config")
TOKEN_FILE = os.path.join(CONFIG_DIR, "token.json")
CLIENT_SECRET_FILE = os.path.join(CONFIG_DIR, "client_secret.json")


class GmailService:
  """Service for sending emails using Gmail API."""
  
  def __init__(self):
    self.creds = None
    self._authenticate()
    
  def _authenticate(self):
    """Authenticate with Gmail API."""
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.
    if os.path.exists(TOKEN_FILE):
      self.creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
      
    # If there are no (valid) credentials available, let the user log in.
    if not self.creds or not self.creds.valid:
      if self.creds and self.creds.expired and self.creds.refresh_token:
        self.creds.refresh(Request())
      else:
        flow = InstalledAppFlow.from_client_secrets_file(
          CLIENT_SECRET_FILE,
          SCOPES
        )
        self.creds = flow.run_local_server(port=0)
        
      # Save the credentials for the next run
      os.makedirs(CONFIG_DIR, exist_ok=True)
      with open(TOKEN_FILE, "w") as token:
        token.write(self.creds.to_json())
        
  def send_email(
    self,
    to: str,
    subject: str,
    body: str,
    attachments: list[str] = None
  ) -> None:
    """
    Send email using Gmail API.
    
    Args:
        to: Recipient email address
        subject: Email subject
        body: Email body text
        attachments: List of file paths to attach
    """
    try:
      service = build("gmail", "v1", credentials=self.creds)
      
      # Create message
      message = MIMEMultipart()
      message["To"] = to
      message["Subject"] = subject
      
      # Add body
      message.attach(MIMEText(body))
      
      # Add attachments
      if attachments:
        for attachment in attachments:
          with open(attachment, "rb") as f:
            part = MIMEApplication(f.read(), Name=os.path.basename(attachment))
            part["Content-Disposition"] = f'attachment; filename="{os.path.basename(attachment)}"'
            message.attach(part)
            
      # Encode and send
      raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode("utf-8")
      service.users().messages().send(
        userId="me",
        body={"raw": raw_message}
      ).execute()
      
    except HttpError as error:
      print(f"An error occurred: {error}")
      raise 