import requests
from ics import Calendar, Event
from datetime import datetime
import pytz

# Your personal API link (only your matches)
url = "https://comet.fsf.fo/data-backend/api/public/areports/run/0/100/?API_KEY=bee18954ec763fa777bd2fc08271eacb0ed09237b37f70949a900a83623e60c6f5a4e23615a7d68554e020ab96b5fcbde7297683e42ecddd079d8b3c9b882f30"
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
