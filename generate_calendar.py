import requests
from ics import Calendar, Event
from datetime import datetime
import pytz

# =========================================
# API URLS
# =========================================

# Your personal referee matches report
matches_url = "https://comet.fsf.fo/data-backend/api/public/areports/run/0/25/?API_KEY=0004RlNG1622b32e32abc567539f1220fc08b1e5bf0efb05fe4eeb725566c9bf8da412e90b1f85903cea3cf1d04a33e718b8a0184b0fc099becfbf01bdf667ab"

# Report with ALL officials on matches
officials_url = "https://comet.fsf.fo/data-backend/api/public/areports/run/0/500/?API_KEY=0004RlNGe23fc15cbacd1c2ce1344810abf6fa0e656443c4de0c2fdb8cb25413c4fefd978f8314637f17a1b243409c829d1c38de01b620d62a7f60d4ec541355"

# =========================================
# FETCH DATA
# =========================================

matches_response = requests.get(matches_url)
matches_data = matches_response.json()

officials_response = requests.get(officials_url)
officials_data = officials_response.json()

# =========================================
# BUILD OFFICIALS DICTIONARY
# =========================================

officials_by_match = {}

for row in officials_data.get("results", []):

    match_id = str(row.get("matchId"))

    if not match_id:
        continue

    person_name = row.get("personName", "Unknown")
    role = row.get("registrationType", "Unknown Role")

    if match_id not in officials_by_match:
        officials_by_match[match_id] = []

    officials_by_match[match_id].append(
        f"{role}: {person_name}"
    )

# =========================================
# CREATE CALENDAR
# =========================================

calendar = Calendar()

tz = pytz.timezone('Atlantic/Faroe')

# =========================================
# LOOP THROUGH YOUR MATCHES
# =========================================

for match in matches_data.get('results', []):

    timestamp = match.get("date")

    if not timestamp:
        continue

    match_id = str(match.get("matchId"))

    description = match.get("matchDescription", "Unknown Match")
    location = match.get("facility", "Unknown Venue")
    competition = match.get("name", "Unknown Competition")
    role = match.get("registrationType", "Unknown Role")
    round_number = match.get("round", "Unknown Round")
    status = match.get("matchStatus", "Unknown Status")

    start = datetime.fromtimestamp(timestamp / 1000, tz)

    # =========================================
    # GET OFFICIALS FOR THIS MATCH
    # =========================================

    officials_text = "No officials found"

    if match_id in officials_by_match:
        officials_text = "\n".join(
            officials_by_match[match_id]
        )

    # =========================================
    # CREATE EVENT
    # =========================================

    event = Event()

    event.name = description

    event.begin = start

    event.duration = {"hours": 2}

    event.location = location

    event.description = (
        f"🏆 {competition}\n"
        f"👤 {role}\n"
        f"🔁 Umfar: {round_number}\n"
        f"📊 Støða: {status}\n\n"
        f"🧑‍⚖️ Dómarar:\n"
        f"{officials_text}"
    )

    calendar.events.add(event)

# =========================================
# WRITE ICS FILE
# =========================================

with open('roi_referee.ics', 'w', encoding='utf-8') as f:
    f.write(str(calendar))

print("Calendar generated successfully!")
