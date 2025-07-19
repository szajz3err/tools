import asyncio
import discord

def spam_channel(token, guild_id):
    channel_id = int(input("ID kanału: "))
    msg = input("Wiadomość do spamu: ")
    print("Spamowanie trwa non stop! Przerwij CTRL+C.")
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    async def endless_spam(channel, message):
        i = 1
        while True:
            try:
                await channel.send(message)
                print(f"Spam! ({i})")
            except Exception as e:
                print(f"Błąd wysyłania: {e}")
            i += 1
            await asyncio.sleep(0.1)  # lekkie opóźnienie by nie wywalić bota na raz

    @client.event
    async def on_ready():
        print(f"Zalogowano jako {client.user}")
        guild = discord.utils.get(client.guilds, id=guild_id)
        if not guild:
            print("Bot nie jest na tym serwerze lub zły guild_id!")
            await client.close()
            return
        channel = guild.get_channel(channel_id)
        if not channel or channel.type != discord.ChannelType.text:
            print("Nie znaleziono kanału tekstowego!")
            await client.close()
            return
        await endless_spam(channel, msg)

    asyncio.run(client.start(token))