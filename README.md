# Curiosity

Curiosity is a Python program that extracts information about users with personal chats in public Telegram groups. The program stores the data in a SQLite database along with their usernames and other relevant information.

## Features

- Connects to Telegram using the Pyrogram library (pyrofork)
- Scans public groups and supergroups
- Identifies users with personal chats
- Stores user information in a SQLite database for users with personal chats
- Handles rate limiting with exponential backoff

## Data Collected

For each user with a personal chat, the following information is stored:

- Username
- Personal chat username
- Source group
- User ID
- Group ID
- Timestamp
- First name
- Last name
- Profile photo URL
- Bio
- Last seen status
- User type
- Group name

## Environment Variables

Refer to the `env_sample` file for the required environment variables. You can copy this file and rename it to `.env`. The following variables are needed:

- API_ID: Your Telegram API ID
- API_HASH: Your Telegram API Hash

## Setup

1. Clone the repository
2. uv sync
3. Set up your `.env` file with the necessary API credentials

## Usage

To run the program, use the following command:

```
python main.py
```

The program will scan through your Telegram dialogs, identify public groups, and collect information about users with personal chats. The data will be stored in a SQLite database named `personal_channels.db`.
