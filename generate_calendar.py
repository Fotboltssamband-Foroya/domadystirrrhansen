import requests
from ics import Calendar, Event
from datetime import datetime, timedelta
import pytz
import sys

# API with real data
url = "https://comet.fsf.fo/data-backend/api/public/areports/run/0/25/?API_KEY=4e1f5586e2e1844730546169899f00ec3005146d2bce2bd40315a12529461c3c9cd6eb39bbb16c1a9d40be1a135adb6289c85812835372eb650dbaa1f86c2485"
response = requests.get(url)

try:
    data = response.json()
except Exception as e:
    print("❌ Failed to decode JSON:", e)
    sys.exit(1)

if "results" not in data:
    print("❌ API response does not contain 'results'. Here's what we got:")
    print(data)
    sys.exit(1)

calendar = Calendar()
tz = pytz.timezone('Atlantic/Faroe')

for match in data['results']:
    description = match.get("matchDescription", "Unknown Match")
    location = match.get("facility", "Unknown Venue")
    timestamp = match.get("matchDate")

    if timestamp:
        try:
            # Convert milliseconds to seconds, then to datetime
            start = datetime.fromtimestamp(timestamp / 1000, tz)
        except Exception as e:
            print(f"⚠️ Could not parse timestamp '{timestamp}':", e)
            continue
    else:
        print(f"⚠️ No matchDate found for match: {description}")
        continue

    event = Event()
    event.name = description
    event.begin = start
    event.duration = {"hours": 2}
    event.location = location
    calendar.events.add(event)

with open('betri_deildin.ics', 'w', encoding='utf-8') as f:
    f.write(str(calendar))
