from discord.ext import commands

class Ready(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.synced = False

    @commands.Cog.listener()
    async def on_ready(self):
        if not self.synced:
            await self.client.tree.sync()
            self.synced = True
            print(f"Sincronizado como {self.client.user}")
        print(f"Bot online: {self.client.user}")

async def setup(client):
    await client.add_cog(Ready(client))