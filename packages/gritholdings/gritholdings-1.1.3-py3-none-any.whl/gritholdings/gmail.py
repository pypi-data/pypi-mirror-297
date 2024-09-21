"""Gmail API Module"""
import pickle
import os.path
import base64
from os import makedirs
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.errors import HttpError


SCOPES = ['https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/gmail.modify']
BASE_URL = '.credentials/gmail/'
CREDENTIALS_PATH = '.credentials/gmail/gmail_api_credentials.json'


class GmailAPIManager:
    """Gmail API Manager"""
    def save_credentials(self, partner_name):
        print(f'Please open the following URL from {partner_name} Gmail Account. It may take '
            f'10-30s for Google to process after Authentication has been completed.')
        flow = InstalledAppFlow.from_client_secrets_file(
            CREDENTIALS_PATH, SCOPES)
        base_path = BASE_URL + partner_name + '/'
        creds = flow.run_local_server(port=0)
        with open(base_path + 'token.pickle', 'wb') as token:
            pickle.dump(creds, token)
            print(f"Successfully saved a new credentials in: {base_path + 'token.pickle'}")


class GmailAPI:
    """Gmail API Class"""
    def __init__(self, partner_name):
        self.partner_name = partner_name # in terms of email address since it's unique
        creds = self._get_credentials()
        self.service = build('gmail', 'v1', credentials=creds)

    def _get_credentials(self):
        creds = None
        base_path = BASE_URL + self.partner_name + '/'
        # create a new folder if it does not exists to avoid error
        if not os.path.exists(base_path):
            makedirs(base_path)
        # source: https://developers.google.com/gmail/api/quickstart/python
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first time.
        if os.path.exists(base_path + 'token.pickle'):
            with open(base_path + 'token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(base_path + 'token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        return creds

    def send_message(self, to: str, subject: str, message: str):
        mime_text = MIMEText(message)
        mime_text['to'] = to
        mime_text['from'] = self.partner_name
        mime_text['subject'] = subject
        raw_message = {'raw': base64.urlsafe_b64encode(mime_text.as_bytes()).decode()}
        try:
            result = self.service.users().messages().send(userId='me', body=raw_message).execute()
            return {'status': 'ok'}
        except Exception as e:
            return e

    def send_html_email(self, to: str, subject: str, body: str):
        try:
            message = MIMEMultipart('alternative')
            message['to'] = to
            message['subject'] = subject

            # Create the HTML version of your message
            html = MIMEText(body, 'html')
            message.attach(html)

            create_message = {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}
            send_message = (self.service.users().messages().send(userId="me", body=create_message).execute())
            print(F'sent message to {to} Message Id: {send_message["id"]}')
        except HttpError as error:
            print(F'An error occurred: {error}')
            return error
        return {'status': 'ok'}
