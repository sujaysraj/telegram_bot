from telegram import Update
from telegram.ext import ContextTypes
import os
import subprocess
import re
import whisper

from utils.fuzzy import fuzzy_lookup
from utils.data import load_data
from commands.tasks import book_meeting, my_tasks
from commands.location import where_is

locations = load_data("data/locations.json")
roles = load_data("data/roles.json")

# Load Whisper model globally
model = whisper.load_model("small")  # Change to "base", "medium", or "large" as needed

# Folder for audio processing
TEMP_DIR = "voices"
os.makedirs(TEMP_DIR, exist_ok=True)

async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    voice = update.message.voice

    ogg_path = f"{TEMP_DIR}/{user.id}_voice.ogg"
    wav_path = f"{TEMP_DIR}/{user.id}_voice.wav"

    # Download and convert
    file = await context.bot.get_file(voice.file_id)
    await file.download_to_drive(ogg_path)

    try:
        subprocess.run(
            ["ffmpeg", "-y", "-i", ogg_path, "-ar", "16000", "-ac", "1", wav_path],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    except subprocess.CalledProcessError:
        await update.message.reply_text("❌ Audio conversion failed.")
        return

    # Transcription using local Whisper
    try:
        result = model.transcribe(wav_path, language='en', temperature=0)
        text = result["text"].strip()
    except Exception as e:
        await update.message.reply_text("⚠️ Transcription failed.")
        print(f"[Whisper Error] {e}")
        return
    finally:
        os.remove(ogg_path)
        os.remove(wav_path)

    # Interpret text
    text_lower = text.lower()
    print(f"🎙 Transcribed: {text_lower}")
    await update.message.reply_text(f"🎙 Transcribed: {text_lower}")

    # Match phrases like "book a meeting with vikas at 8.30 pm"
    if any(keyword in text_lower for keyword in ["book a meeting", "schedule", "set up meeting"]):
        await book_meeting(update, context, text_lower)

    elif "my tasks" in text_lower:
        await my_tasks(update, context)

    elif "where is" in text_lower:
        match = re.search(r"where is (my )?(\w+)", text_lower)
        if match:
            role_name = match.group(2).strip(".?!, ")
            target_id = fuzzy_lookup(role_name, roles)
            if target_id:
                await where_is(update, context, target_id)
            else:
                await update.message.reply_text(f"🤔 I couldn't find anyone like '{role_name}'.")
        else:
            await update.message.reply_text("❗ Try saying: 'Where is my wife?'")

    elif "weather" in text_lower:
        user_id = str(update.effective_user.id)
        user_location = locations.get(user_id)
        if user_location:
            from utils.weather import get_weather
            lat = user_location["lat"]
            lon = user_location["lon"]
            weather_info = get_weather(lat, lon)
            await update.message.reply_text(weather_info)
        else:
            await update.message.reply_text("📍 Please send your location first.")

    else:
        await update.message.reply_text(f"🗣 You said: {text}\nBut I didn't understand that command.")
