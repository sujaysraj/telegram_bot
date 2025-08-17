# Smart Telegram Bot - User Guide

*A comprehensive guide to setting up and using your intelligent Telegram assistant*

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Commands Reference](#commands-reference)
- [Voice Commands](#voice-commands)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

---

## Overview

This Smart Telegram Bot is an intelligent assistant that can help you with:
- **Meeting Scheduling** - Book meetings with Google Calendar integration
- **Location Tracking** - Share and query user locations
- **Voice Commands** - Natural language processing with Whisper AI
- **Task Management** - Store and retrieve personal tasks
- **Role Management** - Manage user roles and permissions
- **Weather Information** - Get weather updates for your location

---

## Features

### Core Functionality
- **Voice Recognition** - Process voice messages using OpenAI's Whisper
- **Natural Language Processing** - Understand conversational commands
- **Google Calendar Integration** - Automatic meeting scheduling
- **Location Services** - Share and track user locations
- **Weather API** - Real-time weather information
- **Role-Based Access** - User role management system

### Security Features
- **Input Validation** - Secure command processing
- **Error Handling** - Graceful failure management
- **Data Protection** - Secure storage of user information
- **API Security** - Secure external service integration

---

## Prerequisites

Before setting up the bot, ensure you have:

### Required Software
- **Python 3.8+** - [Download Python](https://www.python.org/downloads/)
- **FFmpeg** - For audio processing (voice commands)
- **Git** - For cloning the repository

### Required Accounts & APIs
- **Telegram Bot Token** - Create via [@BotFather](https://t.me/botfather)
- **Google Calendar API** - For meeting scheduling
- **OpenWeather API Key** - For weather information
- **AbuseIPDB API Key** - For IP reputation checking

---

## Installation

### 1. Clone the Repository
```bash
git clone <your-repository-url>
cd Telegram_Bot
```

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

If you don't have a requirements.txt file, install these packages:
```bash
pip install python-telegram-bot python-dotenv google-auth google-auth-oauthlib google-api-python-client whisper rapidfuzz dateparser requests
```

### 3. Install FFmpeg
**macOS:**
```bash
brew install ffmpeg
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install ffmpeg
```

**Windows:**
Download from [FFmpeg official website](https://ffmpeg.org/download.html)

---

## Configuration

### 1. Environment Variables
Create a `.env` file in the project root:

```env
# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here

# Weather API
OPENWEATHER_API_KEY=your_openweather_api_key_here

# AbuseIPDB API (for IP reputation)
ABUSEIPDB_API_KEY=your_abuseipdb_api_key_here
```

### 2. Google Calendar Setup
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable Google Calendar API
4. Create credentials (OAuth 2.0 Client ID)
5. Download the credentials file as `credentials.json`
6. Place `credentials.json` in the project root

### 3. Directory Structure
Ensure your project structure looks like this:
```
Telegram_Bot/
├── bot.py
├── .env
├── credentials.json
├── commands/
├── utils/
├── data/
└── voices/
```

---

## Usage

### Starting the Bot
```bash
python bot.py
```

You should see: `🤖 Bot running`

### Basic Interaction
1. **Start a chat** with your bot on Telegram
2. **Send `/start`** to initialize your user profile
3. **Use commands** or **send voice messages** to interact

---

## Commands Reference

### Basic Commands

#### `/start`
Initializes your user profile and saves your details.
```
/start
```
**Response:** Welcome message and profile creation confirmation

#### `/help`
Shows all available commands and their usage.
```
/help
```
**Response:** Complete command list with descriptions

### Role Management

#### `/set_role`
Sets a role and email for a user (requires mentioning the user).
```
/set_role @username role email@example.com
```
**Example:**
```
/set_role @john_doe developer john.doe@company.com
```
**Response:** Confirmation of role assignment

### 📅 Meeting Management

#### `/book_meeting`
Books a meeting with someone at a specific time.
```
/book_meeting time with person
```
**Examples:**
```
/book_meeting 2pm with vikas
/book_meeting 3:30pm with john
```
**Response:** Meeting confirmation and Google Calendar event creation

#### `/my_tasks`
Shows your saved tasks.
```
/my_tasks
```
**Response:** List of your current tasks

### Location Services

#### `/where_is`
Gets the location of a specific user.
```
/where_is @username
```
**Example:**
```
/where_is @vikas
```
**Response:** User's location on map (if they've shared it)

### Sharing Location
Simply send your location to the bot to save it.
- **Mobile:** Use the location sharing feature in Telegram
- **Response:** "📍 Location saved!"

---

## 🎙️ Voice Commands

The bot can understand natural language voice commands. Simply send a voice message and the bot will:

### Meeting Commands
- **"Book a meeting with Vikas at 2pm"**
- **"Schedule a meeting with John at 3:30pm"**
- **"Set up meeting with Sarah at 4pm"**

### Task Commands
- **"My tasks"** - Shows your current tasks
- **"What are my tasks"** - Alternative way to view tasks

### Location Commands
- **"Where is Vikas"** - Gets Vikas's location
- **"Where is my wife"** - Gets location of user with "wife" role

### Weather Commands
- **"What's the weather like"** - Gets weather for your location
- **"Weather"** - Quick weather check

### Example Voice Interactions
```
User: *sends voice message* "Book a meeting with Vikas at 2pm"
Bot: 🎙 Transcribed: book a meeting with vikas at 2pm
Bot: 📅 Meeting booked with Vikas at 2:00 PM.
```

---

## Advanced Features

### Fuzzy Name Matching
The bot uses intelligent name matching, so you can say:
- "Book meeting with vik" (matches "vikas")
- "Where is john" (matches "john_doe")

### Automatic Time Parsing
The bot understands various time formats:
- "2pm", "2:30pm", "14:00", "2 o'clock"
- "tomorrow at 3pm", "next Monday at 10am"

### Google Calendar Integration
When you book a meeting:
1. Bot creates a Google Calendar event
2. Sends invitation to the person's email
3. Confirms the booking with you

---

## Troubleshooting

### Common Issues

#### Bot Not Responding
1. **Check if bot is running:**
   ```bash
   python bot.py
   ```
2. **Verify bot token in .env file**
3. **Check internet connection**

#### Voice Commands Not Working
1. **Ensure FFmpeg is installed:**
   ```bash
   ffmpeg -version
   ```
2. **Check voice file permissions**
3. **Verify Whisper model is downloaded**

#### Google Calendar Issues
1. **Verify credentials.json exists**
2. **Check Google Calendar API is enabled**
3. **Ensure user emails are set with `/set_role`**

#### Weather Not Working
1. **Check OPENWEATHER_API_KEY in .env**
2. **Ensure location is shared first**
3. **Verify API key is valid**

### Error Messages

#### "Couldn't find a match for 'name'"
- Use `/set_role` to add the person first
- Check spelling of the name
- Try using their first name only

#### "Email not found for name"
- Set the person's email using `/set_role`
- Format: `/set_role @username role email@example.com`

#### "Audio conversion failed"
- Ensure FFmpeg is properly installed
- Check file permissions in voices/ directory
- Restart the bot

---

## Data Storage

The bot stores data in JSON files:

### `data/roles.json`
```json
{
  "username": {
    "role": "developer",
    "email": "user@example.com",
    "user_id": 123456789
  }
}
```

### `data/locations.json`
```json
{
  "user_id": {
    "username": "username",
    "latitude": 12.3456,
    "longitude": 78.9012
  }
}
```

### `data/tasks.json`
```json
{
  "user_id": [
    {
      "task": "Meeting with John",
      "timestamp": "2024-01-01T12:00:00"
    }
  ]
}
```

---

## Security & Privacy

### Data Protection
- All data is stored locally in JSON files
- No data is transmitted to third parties (except APIs)
- User IDs are used instead of usernames for privacy

### API Security
- API keys are stored in environment variables
- No hardcoded credentials in the code
- Secure token handling for Google Calendar

### User Privacy
- Location data is only shared when explicitly sent
- Users control what information they share
- No data mining or tracking

---

## Contributing

### Adding New Commands
1. Create a new file in `commands/` directory
2. Follow the existing command structure
3. Add command handler in `bot.py`
4. Update this README

### Adding New Features
1. Create utility functions in `utils/` directory
2. Follow the modular design pattern
3. Add proper error handling
4. Update documentation

### Reporting Issues
- Check the troubleshooting section first
- Provide error messages and logs
- Include steps to reproduce the issue

---

## Support

If you need help:
1. Check this README first
2. Review the troubleshooting section
3. Check the code comments for technical details
4. Create an issue in the repository

---

## License

This project is open source. Feel free to modify and distribute according to your needs.

---

*Happy chatting with your intelligent assistant! 🤖✨*
