import os
import sys
import time
import threading
from tools.mass_dm import mass_dm
from tools.spam_channel import spam_channel
from tools.mass_ban import mass_ban
from tools.channel_tools import delete_channels, create_channels
from tools.webhook_spam import webhook_spam
from tools.server_copy import server_copy
from tools.raid_all import raid_all

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.text import Text
    from rich.prompt import Prompt
    from rich.align import Align
except ImportError:
    print("Please install rich: pip install rich")
    sys.exit(1)

console = Console()
SELECTED_GUILD_ID = None
BOT_TOKEN = None

def set_console_icon(icon_path):
    if os.name != "nt":
        return
    import ctypes
    hwnd = ctypes.windll.kernel32.GetConsoleWindow()
    if hwnd == 0:
        return
    hIcon = ctypes.windll.user32.LoadImageW(0, icon_path, 1, 0, 0, 0x00000010)
    if hIcon == 0:
        return
    WM_SETICON = 0x80
    ctypes.windll.user32.SendMessageW(hwnd, WM_SETICON, 0, hIcon)

def animate_console_title_loop(text="discord.gg/cvel", delay=0.15):
    while True:
        for i in range(len(text) + 1):
            os.system(f"title {text[:i]}")
            time.sleep(delay)
        for i in range(len(text), -1, -1):
            os.system(f"title {text[:i]}")
            time.sleep(delay)

def loading_screen():
    skull = """
            _______
         .-"       "-.
        /             \\
       |  .--. .--.  |
       | (    Y    ) |
        \\  '--'--'  /
         '-._____.-'
    """
    console.clear()
    text = Text(skull, style="bold magenta")
    panel = Panel.fit(
        text,
        border_style="bold magenta",
        title="[bold magenta]DISCORD RAID TOOLS[/bold magenta]",
        subtitle="[bold white]by szajzerr77[/bold white]",
        padding=(1, 4),
    )
    with console.status("[bold magenta]Loading tools...[/bold magenta]", spinner="dots"):
        console.print(panel)
        time.sleep(1.1)
    console.clear()
    console.print(panel)

def menu_panel(selected_guild_id, bot_token):
    menu_text = f"""
[bold magenta]DISCORD RAID TOOLS[/bold magenta]

[bold white]Choose an option below:[/bold white]

[bold magenta]  1.[/bold magenta] Mass DM
[bold magenta]  2.[/bold magenta] Spam Channel (infinite spam)
[bold magenta]  3.[/bold magenta] Mass Ban
[bold magenta]  4.[/bold magenta] Delete Channels
[bold magenta]  5.[/bold magenta] Create Channels / Mass Rename / Categories
[bold magenta]  6.[/bold magenta] Webhook Spam
[bold magenta]  7.[/bold magenta] Server Copy (Backup)
[bold magenta]  8.[/bold magenta] [bold red]RAID ALL - EVERYTHING AT ONCE[/bold red]
[bold magenta]  9.[/bold magenta] [bold cyan]Change server ID[/bold cyan]
[bold magenta] 10.[/bold magenta] [bold cyan]Change bot token[/bold cyan]
[bold magenta]  0.[/bold magenta] [bold red]Exit[/bold red]
"""
    panel = Panel(
        Align.center(menu_text, vertical="middle"),
        border_style="bold magenta",
        title="[bold white]Menu[/bold white]",
        padding=(1, 6),
        width=65
    )
    console.print(panel)

def get_guild_id():
    while True:
        gid = Prompt.ask("[bold magenta]Enter server ID (guild_id)[/bold magenta]")
        if gid.isdigit():
            return int(gid)
        else:
            console.print("[bold red]That is not a number![/bold red]")

def get_token():
    while True:
        t = Prompt.ask("[bold magenta]Enter bot token[/bold magenta]")
        if t and len(t) > 10:
            return t
        else:
            console.print("[bold red]Token too short![/bold red]")

def main_cli():
    global SELECTED_GUILD_ID, BOT_TOKEN

    threading.Thread(target=animate_console_title_loop, daemon=True).start()
    icon_path = os.path.join(os.path.dirname(__file__), "assets", "icon.ico")
    set_console_icon(icon_path)

    loading_screen()
    BOT_TOKEN = get_token()
    SELECTED_GUILD_ID = get_guild_id()

    while True:
        console.clear()
        menu_panel(SELECTED_GUILD_ID, BOT_TOKEN)

        console.print(
            f"\n[bold white]Current token:[/bold white] [bold yellow]{(BOT_TOKEN[:10] + '...' if BOT_TOKEN else 'NOT SET')}[/bold yellow]"
            f"\n[bold white]Current server (guild ID):[/bold white] [bold yellow]{SELECTED_GUILD_ID or 'NOT SET'}[/bold yellow]\n"
        )

        choice = Prompt.ask("\n[bold magenta]Your choice[/bold magenta]", default="0")

        if choice == "0":
            console.print(Panel("[bold red]Get the fuck out![/bold red]", border_style="red", padding=(1, 10)))
            sys.exit(0)

        elif choice == "1":
            mass_dm(BOT_TOKEN, SELECTED_GUILD_ID)
        elif choice == "2":
            spam_channel(BOT_TOKEN, SELECTED_GUILD_ID)
        elif choice == "3":
            mass_ban(BOT_TOKEN, SELECTED_GUILD_ID)
        elif choice == "4":
            delete_channels(BOT_TOKEN, SELECTED_GUILD_ID)
        elif choice == "5":
            create_channels(BOT_TOKEN, SELECTED_GUILD_ID)
        elif choice == "6":
            webhook_spam()
        elif choice == "7":
            server_copy(BOT_TOKEN, SELECTED_GUILD_ID)
        elif choice == "8":
            raid_all(BOT_TOKEN, SELECTED_GUILD_ID)

        elif choice == "9":
            SELECTED_GUILD_ID = get_guild_id()
            console.clear()
            continue

        elif choice == "10":
            BOT_TOKEN = get_token()
            console.clear()
            continue

        else:
            console.print(Panel("[bold yellow]No such option![/bold yellow]", border_style="yellow", padding=(1, 10)))
            time.sleep(1)

if __name__ == "__main__":
    main_cli()
