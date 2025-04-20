import requests
from ics import Calendar, Event
from datetime import datetime, timedelta
import pytz
import sys

# Fetch data from the API
url = "https://comet.fsf.fo/data-backend/api/public/areports/run/0/25/?API_KEY=19fee9cb489e6b3b0ab8e59704ca738ea31c032779e99499e24b8c7f55b57317df241ce808a42f28a44f8a665e326998fa30ad24d0fb603f91882d498ac8e0ce"
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

# Create calendar
calendar = Calendar()
tz = pytz.timezone('Atlantic/Faroe')

# Set a fake base date for demonstration
base_date = datetime(2024, 3, 10)

for i, match in enumerate(data['results']):
    event = Event()
    description = match.get("matchDescription", "Unknown Match")
    location = match.get("facility", "Unknown Venue")

    event.name = description
    event.location = location

    # Simulate dates by round number — you can later replace with real dates if needed
    event.begin = tz.localize(base_date + timedelta(days=i * 7))
    event.duration = {"hours": 2}

    calendar.events.add(event)

# Write to ICS file
with open('betri_deildin.ics', 'w', encoding='utf-8') as f:
    f.write(str(calendar))
