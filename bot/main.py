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

            relative_path = file.relative_to(Path.cwd() if Path.cwd().name != "bot" else Path.cwd().parent)
            module = ".".join(relative_path.with_suffix("").parts)

            try:
                if module not in self.extensions:
                    await self.load_extension(module)
                    print(f"✅ Loaded: {module}")
            except Exception as err:
               print(f"❌ Failed {module}: {err}")

client = MyClient()

def run():
    client.run(TOKEN)