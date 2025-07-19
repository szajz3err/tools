import asyncio
import discord

def delete_channels(token, guild_id):
    limit = int(input("Ile kanałów usunąć (0 = wszystkie): ") or "0")
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
        chans = list(guild.channels)
        count = 0
        for ch in chans:
            try:
                await ch.delete(reason="channelDelete tool")
                print(f"Usunięto {ch.name}")
                count += 1
                if limit and count >= limit:
                    break
            except Exception as e:
                print(f"Błąd usuwania {ch}: {e}")
        await client.close()

    asyncio.run(client.start(token))

def create_channels(token, guild_id):
    qty = int(input("Ile kanałów stworzyć: "))
    base = input("Podstawowa nazwa kanału: ") or "raid"
    create_type = input("Typ (text/voice/category): ").strip().lower()
    change_existing = input("Chcesz masowo zmienić nazwy istniejących kanałów? (t/n): ").strip().lower() == "t"
    change_name = ""
    if change_existing:
        change_name = input("Podaj nową nazwę kanałów: ")

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

        # Tworzenie nowych kanałów/kategorii
        for i in range(qty):
            try:
                if create_type == "text":
                    await guild.create_text_channel(f"{base}-{i}")
                    print(f"Stworzono {base}-{i} (tekstowy)")
                elif create_type == "voice":
                    await guild.create_voice_channel(f"{base}-{i}")
                    print(f"Stworzono {base}-{i} (głosowy)")
                elif create_type == "category":
                    await guild.create_category(f"{base}-{i}")
                    print(f"Stworzono {base}-{i} (kategoria)")
                else:
                    print("Nieznany typ, pomijam...")
            except Exception as e:
                print(f"Błąd tworzenia: {e}")

        # Zmiana nazw istniejących kanałów (masowo)
        if change_existing and change_name:
            print("Masowa zmiana nazw kanałów...")
            for channel in guild.channels:
                try:
                    await channel.edit(name=change_name)
                    print(f"Zmieniono nazwę kanału: {channel.id}")
                except Exception as e:
                    print(f"Błąd zmiany nazwy: {e}")

        await client.close()

    asyncio.run(client.start(token))