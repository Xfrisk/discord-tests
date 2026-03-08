import discord
import typing
from discord.ext import commands
from discord import app_commands

class ServerInfo(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.hybrid_command(name="serverinfo", description="Mostra informações do servidor")
    @app_commands.allowed_installs(users=False, guilds=True)
    @app_commands.allowed_contexts(guilds=True, dms=False, private_channels=True)
    async def serverinfo(self, ctx: commands.Context, server_id: typing.Optional[str] = None):
        if server_id is None:
            guild = ctx.guild
        else:
            try:
                guild_id = int(server_id)

                guild = self.client.get_guild(guild_id)
                if guild is None:
                    guild = await self.client.fetch_guild(guild_id)

            except Exception:
                await ctx.send("❌ Servidor não encontrado ou não tenho acesso a ele.", ephemeral=True)
                return

        if guild is None:
            await ctx.send("❌ Servidor não encontrado.", ephemeral=True)
            return

        owner_id = guild.owner_id

        text_channels = len(guild.text_channels) if hasattr(guild, "text_channels") else "?"
        voice_channels = len(guild.voice_channels) if hasattr(guild, "voice_channels") else "?"
        member_count = guild.member_count if hasattr(guild, "member_count") else "?"

        embed = discord.Embed(
            title="🔑 Informações do Servidor",
            description=f"**{guild.name}**",
            color=discord.Color.blurple()
        )

        embed.add_field(
            name="🪪 ID do Servidor",
            value=f"`{guild.id}`",
            inline=True
        )

        embed.add_field(
            name="👑 Dono",
            value=f"<@{owner_id}>\n(`{owner_id}`)",
            inline=True
        )

        embed.add_field(name="\u200b", value="\u200b", inline=True)

        embed.add_field(
            name="💬 Canais",
            value=f"📝 Texto: {text_channels}\n🔊 Voz: {voice_channels}",
            inline=True
        )

        embed.add_field(
            name="👥 Membros",
            value=f"{member_count}",
            inline=True
        )

        embed.add_field(
            name="📅 Criado em",
            value=f"<t:{int(guild.created_at.timestamp())}:F>",
            inline=True
        )

        if hasattr(guild, "me") and guild.me and guild.me.joined_at:
            embed.add_field(
                name="✨ Entrei aqui em",
                value=f"<t:{int(guild.me.joined_at.timestamp())}:F>",
                inline=False
            )

        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)

        await ctx.send(embed=embed)

async def setup(client: commands.Bot):
    await client.add_cog(ServerInfo(client))