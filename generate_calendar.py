import requests
from ics import Calendar, Event
from datetime import datetime
import pytz
from datetime import datetime, timedeltajsut plasessss

# =========================================
# API URLS
# =========================================

# Your personal referee matches report
matches_url = "https://comet.fsf.fo/data-backend/api/public/areports/run/0/25/?API_KEY=0004RlNG1622b32e32abc567539f1220fc08b1e5bf0efb05fe4eeb725566c9bf8da412e90b1f85903cea3cf1d04a33e718b8a0184b0fc099becfbf01bdf667ab"

# Report with ALL officials on matches
officials_url = "https://comet.fsf.fo/data-backend/api/public/areports/run/0/1000/?API_KEY=0004RlNG489c5a0d8e0e60daf7914e97c5905162e6f6f9ed641645e6e7d1f7c52d53475d15748670eb3fbfe8ec65c466a3b0a133a5e34b8457a9106724ca8603"

# =========================================
# FETCH DATA
# =========================================

matches_response = requests.get(matches_url)
matches_data = matches_response.json()

officials_response = requests.get(officials_url)
officials_data = officials_response.json()

# =========================================
# TIME FILTER
# =========================================

now = datetime.now(tz)

# Keep matches from the last 7 days
# and all future matches
cutoff = now - timedelta(days=7)

# =========================================
# BUILD OFFICIALS DICTIONARY
# =========================================

officials_by_match = {}

for row in officials_data.get("results", []):

    match_id = str(row.get("matchId"))

    if not match_id:
        continue

    # Skip cancelled officials
    role_status = row.get("roleStatus", "")

    if role_status == "CANCELLED":
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

# =========================================
# LOOP THROUGH YOUR MATCHES
# =========================================

for match in matches_data.get('results', []):

    timestamp = match.get("date")

    if not timestamp:
        continue

    start = datetime.fromtimestamp(timestamp / 1000, tz)

    # Skip old matches
    if start < cutoff:
        continue

    match_id = str(match.get("matchId"))

    description = match.get("matchDescription", "Unknown Match")
    location = match.get("facility", "Unknown Venue")
    competition = match.get("name", "Unknown Competition")
    role = match.get("registrationType", "Unknown Role")
    round_number = match.get("round", "Unknown Round")
    status = match.get("matchStatus", "Unknown Status")

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
