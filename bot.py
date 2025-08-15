from telegram.ext import Application, CommandHandler, MessageHandler, filters
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Import command and handler modules
from commands.start import start
from commands.help_cmd import help_command
from commands.roles import set_role
from commands.tasks import book_meeting, my_tasks
from commands.location import handle_location, where_is
from commands.voice import handle_voice

# Setup bot application
app = Application.builder().token(TOKEN).build()

# Command import

## Start command
from commands.start import start

## Help command
from commands.help_cmd import help_command

## Set role command
from commands.roles import set_role

## Set tasks commands
from commands.tasks import book_meeting, my_tasks

## Location commands
from commands.location import handle_location, where_is

## Voice commands
from commands.voice import handle_voice


# Command handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("set_role", set_role))
app.add_handler(CommandHandler("book_meeting", book_meeting))
app.add_handler(CommandHandler("my_tasks", my_tasks))
app.add_handler(CommandHandler("where_is", where_is))

# Message handlers
app.add_handler(MessageHandler(filters.LOCATION, handle_location))
app.add_handler(MessageHandler(filters.VOICE, handle_voice))

# Run the bot
print("🤖 Bot running")
app.run_polling(poll_interval=5)