"""
Get the personal chat of users in a public group and store them in a SQLite database.
"""

import asyncio
import os
import sqlite3
from typing import List, Optional

from pyrogram import Client
from pyrogram.enums import ChatType
from pyrogram.types import Chat, Dialog

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

# Create a table to store usernames and personal chat usernames
c.execute("""
CREATE TABLE IF NOT EXISTS personal_chats (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    personal_chat_username TEXT
)
""")
conn.commit()


async def main() -> None:
    async with app:
        async for dialog in app.get_dialogs():
            if dialog.chat.type in (ChatType.GROUP, ChatType.SUPERGROUP):
                group_id: int = dialog.chat.id

                # Get the group chat
                group_chat: Chat = await app.get_chat(group_id)

                async for member in app.get_chat_members(group_chat.id):
                    user = member.user

                    # Check for personal chat

                    ## Skip bots
                    if user.is_bot:
                        continue

                    try:
                        the_user: Chat = await app.get_chat(user.id)
                        if the_user.type == ChatType.PRIVATE:
                            username: Optional[str] = (
                                the_user.username
                                if the_user.username
                                else str(the_user.id)
                            )
                            personal_chat_username: Optional[str] = (
                                getattr(the_user, "personal_chat", None).username
                                if hasattr(the_user, "personal_chat")
                                else None
                            )
                            if username and personal_chat_username:
                                # Insert username and personal chat username into the database
                                c.execute(
                                    "INSERT OR IGNORE INTO personal_chats (username, personal_chat_username) VALUES (?, ?)",
                                    (username, personal_chat_username),
                                )
                                conn.commit()
                                print(
                                    f"Added {username} with personal chat {personal_chat_username} to the database."
                                )
                    except Exception as e:
                        print(f"Could not get personal chat for {user.id}: {e}")

                    # Wait for 1 second
                    await asyncio.sleep(1)


app.run(main())
