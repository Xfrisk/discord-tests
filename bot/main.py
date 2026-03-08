import discord
from discord.ext import commands
from bot.config import TOKEN
from pathlib import Path

intents = discord.Intents.default()
intents.message_content = True

class MyClient(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="!",
            intents=intents,
            help_command=None
        )

    async def setup_hook(self):
        base_path = Path("bot/cogs")

        for file in base_path.rglob("*.py"):
            if file.name.startswith("__"):
                continue

            module = ".".join(file.with_suffix("").parts)

            try:
                await self.load_extension(module)
                print(f"loaded module {module}")
            except Exception as err:
                print(f"failed to load module {module}: {err}")

client = MyClient()

def run():
    client.run(TOKEN)