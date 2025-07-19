import asyncio
import discord
import json

def server_copy(token, guild_id):
    out_file = input("Plik wyjściowy (np. backup.json): ")
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
        d = {
            "name": guild.name,
            "icon_url": str(guild.icon),
            "roles": [],
            "channels": []
        }
        for role in guild.roles:
            d["roles"].append({
                "name": role.name,
                "permissions": role.permissions.value,
                "color": role.color.value,
                "position": role.position,
                "mentionable": role.mentionable,
                "hoist": role.hoist
            })
        for channel in guild.channels:
            d["channels"].append({
                "name": channel.name,
                "type": str(channel.type),
                "position": channel.position,
                "category": channel.category.name if channel.category else None
            })
        with open(out_file, "w", encoding="utf8") as f:
            json.dump(d, f, ensure_ascii=False, indent=2)
        print(f"Backup zapisany do {out_file}")
        await client.close()

    asyncio.run(client.start(token))