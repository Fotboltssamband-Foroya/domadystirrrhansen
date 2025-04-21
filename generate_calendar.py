import requests
from ics import Calendar, Event
from datetime import datetime
import pytz

url = "https://comet.fsf.fo/data-backend/api/public/areports/run/0/50/?API_KEY=eb76e50daaac67d9cda7413c95c6dcc3074c59bbe2310dd0aff24fb56262e77c8ed6c62503a056b2ccb49eea7fe6b6112da752a80390cff56401d1617caae336"
response = requests.get(url)
data = response.json()

calendar = Calendar()
tz = pytz.timezone('Atlantic/Faroe')

for match in data.get('results', []):
    timestamp = match.get("matchDate")
    if not timestamp:
        continue

    description = match.get("matchDescription", "Ókend dystur")
    location = match.get("facility", "Ókend leikvøllur")
    match_status = match.get("matchStatus", "")
    round_number = match.get("round", "")
    competition = match.get("competitionType", "")

    start = datetime.fromtimestamp(timestamp / 1000, tz)

    event = Event()
    event.name = description
    event.begin = start
    event.duration = {"hours": 2}
    event.location = location
event.description = (
    f"🏆 {competition}\n"
    f"🔁 Umfar: {round_number}\n"
    f"📊 Støða: {match_status}"
)
    calendar.events.add(event)

with open('betri_deildin.ics', 'w', encoding='utf-8') as f:
    f.write(str(calendar))
