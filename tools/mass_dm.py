import asyncio
import discord

def mass_dm(token, guild_id):
    msg = input("Wiadomość do wysłania: ")
    limit = int(input("Ile osób max?: ") or "0")
    intents = discord.Intents.all()
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f"Zalogowano jako {client.user}")
        guild = discord.utils.get(client.guilds, id=guild_id)
        if not guild:
            print("Bot nie jest na tym serwerze lub zły guild_id!")
            await client.close()
            return
        count = 0
        for member in guild.members:
            if member.bot: continue
            try:
                await member.send(msg)
                print(f"Wysłano do {member}")
                count += 0
                if limit and count >= limit:
                    break
            except Exception as e:
                print(f"Blad DM: {member}: {e}")
        await client.close()

    asyncio.run(client.start(token))