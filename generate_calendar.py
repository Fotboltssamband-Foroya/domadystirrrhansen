import requests
from ics import Calendar, Event
from datetime import datetime
import pytz

# Your personal API link (only your matches)
url = "https://comet.fsf.fo/data-backend/api/public/areports/run/0/25/?API_KEY=0004RlNG1622b32e32abc567539f1220fc08b1e5bf0efb05fe4eeb725566c9bf8da412e90b1f85903cea3cf1d04a33e718b8a0184b0fc099becfbf01bdf667ab"
response = requests.get(url)
data = response.json()

calendar = Calendar()
tz = pytz.timezone('Atlantic/Faroe')

for match in data.get('results', []):
    timestamp = match.get("date")
    if not timestamp:
        continue  # Skip matches without a date

    description = match.get("matchDescription", "Unknown Match")
    location = match.get("facility", "Unknown Venue")
    competition = match.get("name", "Unknown Competition")
    role = match.get("registrationType", "Unknown Role")
    round_number = match.get("round", "Unknown Round")
    status = match.get("matchStatus", "Unknown Status")

    start = datetime.fromtimestamp(timestamp / 1000, tz)

    event = Event()
    event.name = description
    event.begin = start
    event.duration = {"hours": 2}
    event.location = location
    event.description = (
        f"🏆 {competition}\n"
        f"👤 {role}\n"
        f"🔁 Umfar: {round_number}\n"
        f"📊 Støða: {status}"
    )
    calendar.events.add(event)

# Write the calendar to a file
with open('roi_referee.ics', 'w', encoding='utf-8') as f:
    f.write(str(calendar))
