import discord
from discord.ext import commands
from discord import app_commands

class Avatar(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.hybrid_command(name="avatar", description="Obtém o avatar do usuário")
    @app_commands.allowed_installs(users=True, guilds=True)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def avatar(self, ctx: commands.Context, user: discord.User):
        embed = discord.Embed(title=f"{user.name} Avatar:")
        embed.set_image(url=f"{user.avatar.url}")

        await ctx.send(embed=embed, ephemeral=bool(ctx.guild))

async def setup(client):
    await client.add_cog(Avatar(client))