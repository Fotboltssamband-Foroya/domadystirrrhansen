import requests
from ics import Calendar, Event
from datetime import datetime
import pytz

API_KEY = "4e1f5586e2e1844730546169899f00ec3005146d2bce2bd40315a12529461c3c9cd6eb39bbb16c1a9d40be1a135adb6289c85812835372eb650dbaa1f86c2485"
BASE_URL = "https://comet.fsf.fo/data-backend/api/public/areports/run/{page}/50/?API_KEY=" + API_KEY

calendar = Calendar()
tz = pytz.timezone('Atlantic/Faroe')

page = 0
total_loaded = 0

while True:
    response = requests.get(BASE_URL.format(page=page))
    data = response.json()
    matches = data.get("results", [])

    if not matches:
        break  # No more matches

    for match in matches:
        description = match.get("matchDescription", "Unknown Match")
        location = match.get("facility", "Unknown Venue")
        timestamp = match.get("matchDate")

        if timestamp:
            start = datetime.fromtimestamp(timestamp / 1000, tz)
        else:
            continue

        event = Event()
        event.name = description
        event.begin = start
        event.duration = {"hours": 2}
        event.location = location
        calendar.events.add(event)
        total_loaded += 1

    page += 1  # Next page

print(f"✅ Loaded {total_loaded} matches")

with open('betri_deildin.ics', 'w', encoding='utf-8') as f:
    f.write(str(calendar))
