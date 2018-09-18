from __future__ import print_function
from apiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools

SCOPES = 'https://www.googleapis.com/auth/calendar'
store = file.Storage('storage.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
    creds = tools.run_flow(flow, store)
GCAL = discovery.build('calendar', 'v3', http=creds.authorize(Http()))

GMT_OFF = '-03:00'      # PDT/MST/GMT-3
EVENT = {
    'summary': 'Dinner with friends',
    'start':  {'dateTime': '2018-09-19T19:00:00%s' % GMT_OFF},
    'end':    {'dateTime': '2018-09-20T22:00:00%s' % GMT_OFF},
    'attendees': [
        {'email': 'reinaldo.sed@gmail.com'},
    ],
}

e = GCAL.events().insert(calendarId='primary',
        sendNotifications=True, body=EVENT).execute()

print('''*** %r event added:
    Start: %s
    End:   %s''' % (e['summary'].encode('utf-8'),
        e['start']['dateTime'], e['end']['dateTime']))
