import requests
from ics import Calendar, Event
from datetime import datetime
import pytz

# API endpoint with the updated API key
url = "https://comet.fsf.fo/data-backend/api/public/areports/run/0/25/?API_KEY=eb76e50daaac67d9cda7413c95c6dcc3074c59bbe2310dd0aff24fb56262e77c8ed6c62503a056b2ccb49eea7fe6b6112da752a80390cff56401d1617caae336"
response = requests.get(url)
data = response.json()

calendar = Calendar()
tz = pytz.timezone('Atlantic/Faroe')

for match in data.get('results', []):
    timestamp = match.get("matchDate")
    if not timestamp:
        continue  # Skip matches without a date

    description = match.get("matchDescription", "Unknown Match")
    location = match.get("facility", "Unknown Venue")

    start = datetime.fromtimestamp(timestamp / 1000, tz)

    event = Event()
    event.name = description
    event.begin = start
    event.duration = {"hours": 2}
    event.location = location
    calendar.events.add(event)

# Write the calendar to a file
with open('betri_deildin.ics', 'w', encoding='utf-8') as f:
    f.write(str(calendar))
