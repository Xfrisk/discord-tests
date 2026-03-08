import discord
from discord.ext import commands
from discord import app_commands
from bot.utils.calcular import calcular


class Math(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.hybrid_command(
        name="math",
        description="Resolve uma expressão matemática"
    )
    @app_commands.allowed_installs(users=True, guilds=True)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)

    async def math(self, ctx: commands.Context, *, expr: str):
        try:
            resultado = calcular(expr)

            embed = discord.Embed(
                title="🧮 Calculadora",
                color=discord.Color.blue()
            )

            embed.add_field(
                name="📥 Expressão",
                value=f"```{expr}```",
                inline=False
            )

            embed.add_field(
                name="📤 Resultado",
                value=f"```{resultado}```",
                inline=False
            )

            embed.set_footer(text=f"Pedido por {ctx.author}")

            await ctx.send(embed=embed)

        except Exception:
            await ctx.send(
                "❌ Expressão inválida.\n"
                "Exemplo: `2 + 3 * (4 - 1)`"
            )


async def setup(client: commands.Bot):
    await client.add_cog(Math(client))