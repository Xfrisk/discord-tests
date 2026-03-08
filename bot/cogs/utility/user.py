import discord
from discord.ext import commands
from discord import app_commands

class User(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.hybrid_command(name="user", description="Retorna as informações do usuário")
    @app_commands.allowed_installs(users=True, guilds=True)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def user(self, ctx: commands.Context, user: discord.User):
        ts = int(user.created_at.timestamp())

        embed = discord.Embed(color=discord.Color.purple())
        embed.set_author(
            name=user.name,
            url=f"https://discord.com/users/{user.id}",
            icon_url=user.display_avatar.url
        )

        embed.description = (
            f"**🆔 ID:** ``{user.id}``\n"
            f"**👤 Usuário:** {user.mention}\n"
            f"**📅 Criado em:** <t:{ts}:f> (<t:{ts}:R>)\n"
        )

        embeds = [embed]

        if bool(ctx.guild):
            member = ctx.guild.get_member(user.id) or await ctx.guild.fetch_member(user.id)

            if member and member.joined_at:
                ts_joined = int(member.joined_at.timestamp())
                
                embed2 = discord.Embed(color=discord.Color.pink())
                embed2.title = member.display_name
                embed2.set_thumbnail(url=member.display_avatar.url)
                
                embed2.description = (
                    f"**📅 Entrou no servidor em:**\n"
                    f"<t:{ts_joined}:f> (<t:{ts_joined}:R>)"
                )
                
                embeds.append(embed2)

        await ctx.send(embeds=embeds, ephemeral=bool(ctx.guild))

async def setup(client: commands.Bot):
    await client.add_cog(User(client))