from discord.ext import commands
import discord

class Ready(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.synced = False 

    @commands.Cog.listener()
    async def on_ready(self):
        if not self.synced:
            await self.client.tree.sync()
            self.synced = True
            print(f"slash commands synced")
        
        print(f"bot on as {self.client.user} (ID: {self.client.user.id})")

async def setup(client):
    await client.add_cog(Ready(client))