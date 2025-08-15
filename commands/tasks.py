from telegram import Update
from telegram.ext import ContextTypes
import json, datetime, re
from utils.calendar import get_calendar_service, create_event
from utils.data import load_data
from utils.fuzzy import fuzzy_lookup
import dateparser
import datetime

TASKS_FILE = "tasks.json"
roles = load_data("data/roles.json")

def load_tasks():
    try:
        return json.load(open(TASKS_FILE))
    except:
        return {}

tasks = load_tasks()

def parse_time_string(time_str):
    parsed_time = dateparser.parse(time_str, settings={'PREFER_DATES_FROM': 'future'})
    if not parsed_time:
        raise ValueError(f"Couldn't parse time: {time_str}")

    return parsed_time.replace(second=0, microsecond=0)


async def book_meeting(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str):
    print("DEBUG: roles keys =", list(roles.keys()))
    text = text.lower()

    # Extract name and time from the sentence
    name_match = re.search(r"with ([\w\s]+?) at", text)
    time_match = re.search(r'\b(\d{1,2}[:.]?\d{0,2}\s?(?:am|pm)?)\b', text, re.IGNORECASE)

    if not name_match or not time_match:
        await update.message.reply_text("❗ I couldn't extract the name or time. Please try again.")
        return

    name = name_match.group(1).strip()
    time_str = time_match.group(1).strip()

    # Fuzzy match name to role
    matched_user_id = fuzzy_lookup(name, roles)
    if not matched_user_id:
        await update.message.reply_text(f"❗ Couldn’t find a match for '{name}' in saved roles.")
        return

    role_info = roles[matched_user_id]
    invite_email = role_info.get("email")

    if not invite_email:
        await update.message.reply_text(f"❗ Email not found for {name}. Please set it using /set_role.")
        return

    try:
        print(f"[DEBUG] Raw time string = '{time_str}'")
        start_dt = parse_time_string(time_str)
    except ValueError:
        await update.message.reply_text(f"❗ Couldn't parse time: {time_str}")
        return

    end_dt = start_dt + datetime.timedelta(minutes=30)

    event = create_event(
        summary=f"Meeting with {name.title()}",
        description="Scheduled via assistant",
        start_dt=start_dt,
        end_dt=end_dt,
        attendees=[invite_email],
        service=get_calendar_service()  # Make sure this returns a valid service object
    )

    await update.message.reply_text(f"📅 Meeting booked with {name.title()} at {start_dt.strftime('%I:%M %p')}.")

async def my_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    user_tasks = tasks.get(user_id, [])
    if not user_tasks:
        await update.message.reply_text("📭 No tasks found.")
    else:
        text = '\n'.join([f"🗓 {t['task']}" for t in user_tasks])
        await update.message.reply_text(text)
