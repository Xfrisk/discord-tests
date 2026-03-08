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
        current_dir = Path(__file__).parent
        base_path = current_dir / "cogs"
        
        project_root = current_dir.parent

        print("--- loading cogs ---")
        for file in base_path.rglob("*.py"):
            if file.name.startswith("__"):
                continue

            try:
                relative_path = file.relative_to(project_root)
                module = ".".join(relative_path.with_suffix("").parts)

                if module not in self.extensions:
                    await self.load_extension(module)
                    print(f"loaded: {module}")
                else:
                    print(f"cog is already loaded: {module}")
            except Exception as err:
                print(f"error while loading {file.name}: {err}")
        print("--------------------------")

client = MyClient()

def run():
    client.run(TOKEN)