
""" Интеграция с Google Calendar """


from __future__ import annotations
from typing import List, Dict
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import datetime
import os


class GoogleCalendarIntegration:
    def __init__(
        self,
        credentials_path: str = 'src/app/integrations/credentials.json'
    ):
        self.SCOPES = ["https://www.googleapis.com/auth/calendar"]
        self.creds = None
        self.service = None
        self.credentials_path = credentials_path
        self.token_path = "./token.json"

    def authenticate(self):
        """Авторизация и настройка службы."""
        if os.path.exists(self.token_path):
            self.creds = Credentials.from_authorized_user_file(
                self.token_path, self.SCOPES)

        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, self.SCOPES)
                self.creds = flow.run_local_server(port=0)

            with open(self.token_path, 'w') as token:
                token.write(self.creds.to_json())

        self.service = build('calendar', 'v3', credentials=self.creds)

    def get_upcoming_events(self, num_events: int = 10) -> List[Dict]:
        """Возвращает ближайшие события из календаря."""
        self.authenticate()
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        result = self.service.events().list(
            calendarId="primary",
            timeMin=now,
            maxResults=num_events,
            singleEvents=True,
            orderBy="startTime"
        ).execute()
        return result.get("items", [])

    def create_event(
        self,
        summary: str,
        location: str,
        description: str,
        start_time: str,
        end_time: str
    ):
        """Создание нового события в календаре."""
        event = {
            "summary": summary,
            "location": location,
            "description": description,
            "start": {"dateTime": start_time},
            "end": {"dateTime": end_time},
        }
        created_event = self.service.events().insert(
            calendarId="primary", body=event).execute()
        return created_event.get("id")


# Пример использования
if __name__ == "__main__":
    integration = GoogleCalendarIntegration()
    upcoming_events = integration.get_upcoming_events(num_events=5)
    print(upcoming_events)
