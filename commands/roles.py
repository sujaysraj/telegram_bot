from telegram import Update
from telegram.ext import ContextTypes
from utils.data import load_data, save_data

ROLES_FILE = "data/roles.json"
roles = load_data(ROLES_FILE)

async def set_role(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 3:
        await update.message.reply_text("Usage: /set_role @username role email@example.com")
        return

    if update.message.entities and len(update.message.entities) > 1:
        entity = update.message.entities[1]
        if entity.user:
            user = entity.user
            name_key = user.first_name.lower()  # You can change this to user.username.lower() if preferred
            role_value = context.args[1].lower()
            email_value = context.args[2].strip()

            roles[name_key] = {
                "role": role_value,
                "email": email_value,
                "user_id": user.id
            }

            # ✅ This line saves the updated data
            save_data(ROLES_FILE, roles)

            await update.message.reply_text(
                f"✅ Role set:\n👤 Name: {user.first_name}\n🎭 Role: {role_value}\n📧 Email: {email_value}"
            )
        else:
            await update.message.reply_text("❌ Could not resolve user from mention.")
    else:
        await update.message.reply_text("❌ Please mention a user like: /set_role @username role email@example.com")
