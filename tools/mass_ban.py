import asyncio
import discord

def mass_ban(token, guild_id):
    role_name = input("Nazwa roli do banowania: ")
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
        role = discord.utils.get(guild.roles, name=role_name)
        if not role:
            print("Nie znaleziono roli")
            await client.close()
            return
        count = 0
        for member in role.members:
            try:
                await member.ban(reason="massBan tool")
                print(f"Zbanowano {member}")
                count += 1
                if limit and count >= limit:
                    break
            except Exception as e:
                print(f"Blad banowania {member}: {e}")
        await client.close()

    asyncio.run(client.start(token))