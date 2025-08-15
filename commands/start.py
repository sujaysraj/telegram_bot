from telegram import Update
from telegram.ext import ContextTypes
from utils.data import load_data, save_data

ROLES_FILE = "data/roles.json"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    name_key = user.first_name.lower()

    roles = load_data(ROLES_FILE)

    if name_key not in roles:
        roles[name_key] = {
            "role": "unknown",
            "email": None,
            "user_id": user.id
        }
        save_data(ROLES_FILE, roles)
        await update.message.reply_text(f"👋 Hello {user.first_name}! Your details have been saved.")
    else:
        await update.message.reply_text(f"👋 Welcome back, {user.first_name}!")
