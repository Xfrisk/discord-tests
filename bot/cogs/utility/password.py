import secrets
import random
from discord.ext import commands
from discord import app_commands

class Password(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.hybrid_command(name="password", description="Gera uma senha aleatória segura")
    @app_commands.allowed_installs(users=True, guilds=True)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.describe(
        chars="Comprimento total da senha (padrão: 12)",
        incluir_especiais="Usar !@#$%^&* ?",
        incluir_numeros="Usar números 0-9?",
        incluir_maiusculas="Usar letras maiúsculas A-Z?",
        min_especiais="Quantidade mínima de símbolos (padrão: 1)",
        min_numeros="Quantidade mínima de números (padrão: 1)",
        evitar_ambiguos="Remove caracteres confusos como l, I, 1, 0, O"
    )
    async def password(
        self, 
        ctx: commands.Context, 
        chars: int = 12, 
        incluir_especiais: bool = True, 
        incluir_numeros: bool = True, 
        incluir_maiusculas: bool = True,
        min_especiais: int = 1,
        min_numeros: int = 1,
        evitar_ambiguos: bool = True
    ):
        letras_base = "abcdefghijklmnopqrstuvwxyz"
        letras_upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ" if incluir_maiusculas else ""
        digitos = "0123456789" if incluir_numeros else ""
        simbolos = "!@#$%^&*" if incluir_especiais else ""

        if evitar_ambiguos:
            for c in "lI1oO0":
                letras_base = letras_base.replace(c, "")
                letras_upper = letras_upper.replace(c, "")
                digitos = digitos.replace(c, "")

        pool_total = letras_base + letras_upper + digitos + simbolos
        
        if not pool_total:
            return await ctx.send("❌ Erro: Selecione pelo menos um tipo de caractere!", ephemeral=True)

        resultado = []
        
        if incluir_especiais and min_especiais > 0:
            resultado += [secrets.choice(simbolos) for _ in range(min_especiais)]
        
        if incluir_numeros and min_numeros > 0:
            resultado += [secrets.choice(digitos) for _ in range(min_numeros)]

        if len(resultado) > chars:
            return await ctx.send(f"❌ Erro: O tamanho total ({chars}) é menor que a soma dos mínimos exigidos!", ephemeral=True)

        while len(resultado) < chars:
            resultado.append(secrets.choice(pool_total))

        random.shuffle(resultado)
        senha_final = "".join(resultado)

        await ctx.send(f"### 🔐 Sua senha gerada:\n`{senha_final}`", ephemeral=True)

async def setup(client: commands.Bot):
    await client.add_cog(Password(client))