from telegram import Update
from telegram.ext import ContextTypes
import json, os

LOCATIONS_FILE = "data/locations.json"

def load_locations():
    if os.path.exists(LOCATIONS_FILE):
        with open(LOCATIONS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_locations(data):
    with open(LOCATIONS_FILE, 'w') as f:
        json.dump(data, f, indent=2)

locations = load_locations()

async def handle_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    location = update.message.location
    if not location:
        return

    locations[str(user.id)] = {
        "username": user.username or user.first_name,
        "latitude": location.latitude,
        "longitude": location.longitude,
    }
    save_locations(locations)

    await update.message.reply_text("📍 Location saved!")

async def where_is(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /where_is @username")
        return

    username = context.args[0].lstrip('@')
    for user_id, info in locations.items():
        if info["username"] == username:
            lat = info["latitude"]
            lon = info["longitude"]
            await update.message.reply_location(latitude=lat, longitude=lon)
            return

    await update.message.reply_text("❓ Couldn't find that user's location.")
