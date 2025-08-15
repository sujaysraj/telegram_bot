from telegram import Update
from telegram.ext import ContextTypes

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "🤖 Bot Commands:\n"
        "/start - Start the bot\n"
        "/set_role @username role - Set a role for a user\n"
        "/book_meeting time with person - Book a meeting\n"
        "/my_tasks - View your tasks\n"
        "/where_is @username - Get location of a user\n"
        "/help - Show this help message"
    )
    await update.message.reply_text(help_text)
