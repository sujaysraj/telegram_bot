import re
from datetime import datetime, timedelta

def extract_meeting_details(text):
    """
    Very basic NLP logic to extract name and time from phrases like:
    "book a meeting with John at 8:30 pm"
    Returns dict: {"name": "John", "time": "2025-06-12T20:30:00"}
    """
    name_match = re.search(r"(?:with|meet|meeting with)\s+(\w+)", text)
    time_match = re.search(r"at\s+(\d{1,2}(?::\d{2})?\s*(?:am|pm)?)", text)

    if not name_match or not time_match:
        return None

    name = name_match.group(1)
    time_str = time_match.group(1)

    try:
        time_obj = datetime.strptime(time_str, "%I:%M %p") if ":" in time_str else datetime.strptime(time_str, "%I %p")
    except ValueError:
        return None

    # Assume meeting is today unless already passed
    now = datetime.now()
    meeting_time = now.replace(hour=time_obj.hour, minute=time_obj.minute, second=0, microsecond=0)
    if meeting_time < now:
        meeting_time += timedelta(days=1)

    return {
        "name": name,
        "time": meeting_time.isoformat()
    }