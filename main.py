"""
Get the personal chat of users in a public group and store them in a SQLite database.
"""

import asyncio
import os
import sqlite3
from typing import Optional
from datetime import datetime

from pyrogram import Client
from pyrogram.enums import ChatType
from pyrogram.types import Chat
from pyrogram.errors import FloodWait

from dotenv import load_dotenv

load_dotenv()
API_ID: str = os.getenv("API_ID")
API_HASH: str = os.getenv("API_HASH")

assert API_ID, "Please set the API_ID environment variable."
assert API_HASH, "Please set the API_HASH environment variable."

app: Client = Client("curiosity", api_id=API_ID, api_hash=API_HASH)

# Create or connect to the SQLite database
conn: sqlite3.Connection = sqlite3.connect("personal_channels.db")
c: sqlite3.Cursor = conn.cursor()

# Create a table to store usernames, personal chat usernames, and source
c.execute("""
CREATE TABLE IF NOT EXISTS personal_chats (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    personal_chat_username TEXT,
    source TEXT,
    user_id INTEGER,
    group_id INTEGER,
    timestamp TEXT,
    first_name TEXT,
    last_name TEXT,
    profile_photo_url TEXT,
    bio TEXT,
    last_seen_status TEXT,
    user_type TEXT,
    group_name TEXT
)
""")
conn.commit()


async def main() -> None:
    async with app:
        async for dialog in app.get_dialogs():
            if dialog.chat.type in (ChatType.GROUP, ChatType.SUPERGROUP):
                group_id: int = dialog.chat.id
                group_username: str = (
                    dialog.chat.username if dialog.chat.username else str(group_id)
                )
                group_name: str = (
                    dialog.chat.title if dialog.chat.title else "Unknown Group"
                )

                # Get the group chat
                group_chat: Chat = await app.get_chat(group_id)

                async for member in app.get_chat_members(group_chat.id):
                    user = member.user

                    # Check for personal chat

                    ## Skip bots
                    if user.is_bot:
                        continue

                    backoff_time = 1  # Start with a 1 second backoff
                    while True:
                        try:
                            the_user: Chat = await app.get_chat(user.id)
                            if the_user:
                                if the_user.type == ChatType.PRIVATE:
                                    # Debug prints
                                    print(f"User ID: {the_user.id}")
                                    print(f"Username from the_user: {the_user.username}")
                                    print(f"Username from user: {user.username}")
                                        
                                    username: Optional[str] = (
                                        user.username or the_user.username or str(the_user.id)
                                    )
                                    personal_chat = getattr(the_user, "personal_chat", None)
                                    personal_chat_username: Optional[str] = (
                                        personal_chat.username if personal_chat else None
                                    )
                                    first_name: Optional[str] = the_user.first_name
                                    last_name: Optional[str] = the_user.last_name
                                    profile_photo_url: Optional[str] = (
                                        the_user.photo.big_file_id
                                        if the_user.photo
                                        else None
                                    )

                                    # download the profile photo
                                    if profile_photo_url:
                                        profile_photo = await app.download_media(
                                            profile_photo_url
                                        )
                                        profile_photo_url = profile_photo

                                    bio: Optional[str] = (
                                        the_user.bio if hasattr(the_user, "bio") else None
                                    )
                                    last_seen_status: Optional[str] = str(member.status)
                                    user_type: Optional[str] = (
                                        "bot" if user.is_bot else "user"
                                    )
                                    timestamp: str = datetime.now().isoformat()

                                    # Insert all information into the database
                                    c.execute(
                                        "INSERT OR IGNORE INTO personal_chats (username, personal_chat_username, source, user_id, group_id, timestamp, first_name, last_name, profile_photo_url, bio, last_seen_status, user_type, group_name) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                        (
                                            username,
                                            personal_chat_username,
                                            group_username,
                                            user.id,
                                            group_id,
                                            timestamp,
                                            first_name,
                                            last_name,
                                            profile_photo_url,
                                            bio,
                                            last_seen_status,
                                            user_type,
                                            group_name,
                                        ),
                                    )
                                    conn.commit()
                                    print(
                                        f"Added {username} with personal chat {personal_chat_username or 'None'} from {group_username} to the database."
                                    )
                                break  # Exit the loop if successful
                        except FloodWait:
                            print(
                                f"Rate limit exceeded. Waiting for {backoff_time} seconds."
                            )
                            await asyncio.sleep(backoff_time)
                            backoff_time *= 2  # Exponential backoff
                        except Exception as e:
                            print(
                                f"Could not get personal chat for{type(user)}:{user.id}: {e}"
                            )
                            break  # Exit the loop on other exceptions

                    # Wait for 1 second
                    await asyncio.sleep(1)


app.run(main())
