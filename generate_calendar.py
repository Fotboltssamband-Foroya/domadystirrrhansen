import requests
from ics import Calendar, Event
from datetime import datetime
import pytz

# Fetch data from the API
response = requests.get("https://comet.fsf.fo/data-backend/api/public/areports/run/0/25/?API_KEY=19fee9cb489e6b3b0ab8e59704ca738ea31c032779e99499e24b8c7f55b57317df241ce808a42f28a44f8a665e326998fa30ad24d0fb603f91882d498ac8e0ce")
data = response.json()

# Create a new calendar
calendar = Calendar()

# Timezone for Faroe Islands
tz = pytz.timezone('Atlantic/Faroe')

# Process each match
for match in data['data']:
    event = Event()
    event.name = f"{match['homeTeam']} vs {match['awayTeam']}"
    start_time = datetime.strptime(match['matchDate'], "%Y-%m-%dT%H:%M:%S")
    event.begin = tz.localize(start_time)
    event.location = match['venue']
    calendar.events.add(event)

# Write to .ics file
with open('betri_deildin.ics', 'w') as f:
    f.writelines(calendar)
