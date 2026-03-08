from discord.ext import commands
import discord

class Ready(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.tree.sync()

async def setup(client):
    await client.add_cog(Ready(client))