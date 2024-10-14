from pyrogram import Client

app = Client("my_account")


async def main():
    async with app:
        # "me" refers to your own chat (Saved Messages)
        async for message in app.get_chat_history("me"):
            print(message)


app.run(main())