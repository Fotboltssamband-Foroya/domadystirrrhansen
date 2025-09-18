import requests
from ics import Calendar, Event
from datetime import datetime
import pytz

# Your personal API link (only your matches)
url = "https://comet.fsf.fo/data-backend/api/public/areports/run/0/100/?API_KEY=1300785ded072b2ad22503876d061835806194b1f56bc52de0026346c9b0c5a392ddf5c5864c2a17bc7cfb2e3745cd01381cbc7a50ebddb73c785059b10a55d7"
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
