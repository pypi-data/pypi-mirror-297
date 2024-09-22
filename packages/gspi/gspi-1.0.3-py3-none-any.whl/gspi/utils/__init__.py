import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def generate_token(creds_file,token_file):
    creds = None
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
    if os.path.isfile(token_file):
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(creds_file, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_file, 'w') as token:
            token.write(creds.to_json())
    return creds

def generate_token_from_json(creds_info,token_info):
    creds = None
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
    if token_info:
        creds = Credentials.from_authorized_user_info(token_info, SCOPES)
        new_token_info = token_info
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(creds_info, SCOPES)
            creds = flow.run_local_server(port=0)
        new_token_info = creds.to_json()
    return creds, new_token_info