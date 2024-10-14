"""
get the personal channel of a user
"""
import asyncio
import os

from pyrogram import Client
from pyrogram.enums import ChatType

API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
CHANNEL_HANDLE = os.getenv('CHANNEL_HANDLE')
ENDPOINT_URL = os.getenv('ENDPOINT_URL')

app = Client("ooredoobot", api_id=API_ID, api_hash=API_HASH)


async def main():
    async with app:
        async for dialog in app.get_dialogs():
            # only process actual users
            if dialog.chat.type == ChatType.PRIVATE:
                print(dialog.chat.title or dialog.chat.first_name)

                print(dialog.chat.personal_chat)

                # get the user
                chat = await app.get_chat(chat_id=dialog.chat.id)
                with open(f'users/{chat.id}.json', 'w') as f:
                    f.write(str(chat))

                # wait for 4 seconds
                await asyncio.sleep(4)
            # await asyncio.sleep(1)

app.run(main())
