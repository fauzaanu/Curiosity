"""
Get the personal chat of users in a public group and store them in a SQLite database.
"""
import asyncio
import os
import sqlite3

from pyrogram import Client
from pyrogram.enums import ChatType

from dotenv import load_dotenv

load_dotenv()
API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
GROUP_USERNAME = os.getenv('GROUP_USERNAME')

app = Client("ooredoobot", api_id=API_ID, api_hash=API_HASH)

# Create or connect to the SQLite database
conn = sqlite3.connect('users.db')
c = conn.cursor()

# Create a table to store usernames and personal chat usernames
c.execute('''
CREATE TABLE IF NOT EXISTS personal_chats (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    personal_chat_username TEXT
)
''')
conn.commit()


async def main():
    async with app:
        # Get the group chat
        group_chat = await app.get_chat(str(GROUP_USERNAME))

        # Ensure the chat is a group
        if group_chat.type == ChatType.GROUP or group_chat.type == ChatType.SUPERGROUP:
            async for member in app.get_chat_members(group_chat.id):
                user = member.user

                # Check for personal chat
                if user.is_bot:
                    continue

                try:
                    user_chat = await app.get_chat(user.id)
                    if user_chat.type == ChatType.PRIVATE:
                        username = user.username
                        personal_chat_username = user_chat.username
                        if username and personal_chat_username:
                            # Insert username and personal chat username into the database
                            c.execute('INSERT OR IGNORE INTO personal_chats (username, personal_chat_username) VALUES (?, ?)', (username, personal_chat_username))
                            conn.commit()
                            print(f"Added {username} with personal chat {personal_chat_username} to the database.")
                except Exception as e:
                    print(f"Could not get personal chat for {user.id}: {e}")

                # Wait for 4 seconds
                await asyncio.sleep(4)

app.run(main())
