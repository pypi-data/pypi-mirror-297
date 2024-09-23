import os
import json
from googleapiclient.discovery import build
from google.oauth2 import service_account


class GoogleCalendar:

    def __init__(self, calendarId):
        self.calendarId = calendarId
        self._creds = None
        self._service = None

    @property
    def creds(self):
        if self._creds is None:
            creds_json = os.environ["GOOGLE_CALENDAR_CREDENTIALS"]
            if creds_json:
                self._creds = service_account.Credentials.from_service_account_info(
                    json.loads(creds_json))
        return self._creds

    @property
    def service(self):
        if self._service is None and self.creds:
            self._service = build("calendar",
                                  "v3",
                                  credentials=self.creds,
                                  cache_discovery=False)
        return self._service

    def list_events(self, start_date):
        """
        :param start_date: The date filter for the events. Expects an ISO formatted date object
        Example          : pendulum.datetime(2020, 9, 1).isoformat()

        :return: Dictionary of event items
        """

        page_token = None
        events = []
        count = 0

        while True:
            # Remember that maxResults does not guarantee the number of results on one page
            # Use pagination instead: https://developers.google.com/calendar/v3/pagination
            # Code for generating page tokens: https://developers.google.com/calendar/v3/reference/calendarList/list#python
            events_list = self.service.events().list(
                calendarId=self.calendarId,
                pageToken=page_token,
                timeMin=start_date,
                maxResults=100,
                singleEvents=True,
                orderBy='startTime').execute()

            for event in events_list['items']:
                events.append(event)

            page_token = events_list.get('nextPageToken')

            count += 1

            print(f"Google Calendar: Fetching results from page {count} ...")

            if not page_token:
                break

        print(f"Fetched a total of {len(events)} events.")
        return events
