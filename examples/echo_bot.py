from pyrogram import Client, filters

app = Client("my_account")


@app.on_message(filters.text & filters.private)
async def echo(client, message):
    await message.reply(message.text)


app.run()  # Automatically start() and idle()