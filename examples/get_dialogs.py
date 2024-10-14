from pyrogram import Client

app = Client("my_account")


async def main():
    async with app:
        async for dialog in app.get_dialogs():
            print(dialog.chat.title or dialog.chat.first_name)


app.run(main())