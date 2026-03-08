from discord.ext import commands
from discord import app_commands

class Ping(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.hybrid_command(name="ping", description="Mostra a latência do bot")
    @app_commands.allowed_installs(users=True, guilds=True)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def ping(self, ctx):
        await ctx.send(f"🏓 Pong! {round(self.client.latency * 1000)}ms", ephemeral=bool(ctx.guild))

async def setup(client):
    await client.add_cog(Ping(client))