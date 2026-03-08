import discord
import typing
from discord.ext import commands
from discord import app_commands

class ServerIcon(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.hybrid_command(name="servericon", description="Obtém o ícone do servidor")
    @app_commands.allowed_installs(users=False, guilds=True)
    @app_commands.allowed_contexts(guilds=True, dms=False, private_channels=True)
    async def servericon(self, ctx: commands.Context, server_id: typing.Optional[str]):
        if server_id is None:
            guild = ctx.guild
        else:
            try:
                guild_id = int(server_id)
                guild = self.client.get_guild(guild_id)

                if guild is None:
                    guild = await self.client.fetch_guild(guild_id)
            except Exception:
                await ctx.send("Servidor não encontrado ou não tenho acesso a ele.", ephemeral=True)
                return

        if not guild or not guild.icon:
            name = guild.name if guild else "Este servidor"
            await ctx.send(f"O servidor **{name}** não possui um ícone ou não foi encontrado!", ephemeral=True)
            return

        embed = discord.Embed(title=f"{ctx.guild.name} icon:")
        embed.set_image(url=guild.icon.url)
        await ctx.send(embed=embed, ephemeral=True)

async def setup(client):
    await client.add_cog(ServerIcon(client))