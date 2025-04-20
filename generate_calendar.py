import requests
from ics import Calendar, Event
from datetime import datetime
import pytz

# API endpoint
url = "https://comet.fsf.fo/data-backend/api/public/areports/run/0/25/?API_KEY=84d9dc643e99879cb5ee2213b56a4094346c72c452d47cd4c029c27c6695f74c27d073d7d8327e0092cd84a9ac1eb77999c35ae7e61f6911fc72284280798f35"
response = requests.get(url)
data = response.json()

calendar = Calendar()
tz = pytz.timezone('Atlantic/Faroe')

for match in data.get("results", [])[:1]:
    print(match)

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

with open('betri_deildin.ics', 'w', encoding='utf-8') as f:
    f.write(str(calendar))
