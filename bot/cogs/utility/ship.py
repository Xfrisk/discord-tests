import discord
from discord.ext import commands
from discord import app_commands
from PIL import Image, ImageDraw, ImageFont
import aiohttp
import io
import random
import asyncio
from pathlib import Path

ASSETS_PATH = Path(__file__).parent.parent.parent / "assets" / "ship"

# ─────────────── TIER CONFIG ───────────────
TIERS = [
    {
        "range": (0, 25),
        "bg_file": "bg_0.png",
        "bar": (200, 50, 50),
        "messages": [
            "Essa dupla não tem futuro... 💔",
            "Nem como amigos tá fácil.",
            "O universo disse não. ❌",
            "Água e óleo. Não rola.",
            "Até os astros estão rindo. 😂",
        ],
    },
    {
        "range": (26, 50),
        "bg_file": "bg_1.png",
        "bar": (190, 150, 50),
        "messages": [
            "Pode ser... mas vai precisar de esforço. 🤔",
            "50/50. O destino vai decidir.",
            "Talvez com tempo? Quem sabe.",
            "Não é impossível, mas não é fácil.",
            "Tem potencial, mas precisa trabalhar nisso.",
        ],
    },
    {
        "range": (51, 75),
        "bg_file": "bg_2.png",
        "bar": (220, 80, 120),
        "messages": [
            "Tem química sim! 💕",
            "Quase lá! Só falta coragem. 🌸",
            "O coração tá acelerando! 💓",
            "Tão perto de ser oficial... 👀",
            "Alguém aqui tá apaixonado e não assumiu ainda. 🥀",
        ],
    },
    {
        "range": (76, 100),
        "bg_file": "bg_3.png",
        "bar": (255, 50, 100),
        "messages": [
            "CASAL PERFEITO! 💖✨",
            "O destino já decidiu! 💘",
            "Alguém chama o padre! 💒",
            "Compatibilidade máxima! Casem logo! 👰🤵",
            "Nem o tempo separa vocês dois. 🔥",
        ],
    },
]

AV_SIZE  = 159
AV_LEFT  = (25, 64)
AV_RIGHT = (342, 64)

FONT_PATH = Path(__file__).parent.parent.parent / "assets" / "ship" / "Roboto-Bold.ttf"

SCALE = 1

def get_percent(id1: int, id2: int) -> int:
    low, high = min(id1, id2), max(id1, id2)
    return (low ^ high ^ (low + high)) % 101

def get_ship_name(name1: str, name2: str) -> str:
    half1 = name1[: max(1, len(name1) // 2)]
    half2 = name2[max(0, len(name2) // 2):]
    return (half1 + half2).lower()

async def fetch_avatar(session: aiohttp.ClientSession, url: str, size: int = AV_SIZE) -> Image.Image:
    async with session.get(url) as resp:
        data = await resp.read()
    size_s = size * SCALE
    img = Image.open(io.BytesIO(data)).convert("RGBA").resize((size_s, size_s), Image.LANCZOS)
    mask = Image.new("L", (size_s, size_s), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, size_s - 1, size_s - 1), fill=255)
    result = Image.new("RGBA", (size_s, size_s), (0, 0, 0, 0))
    result.paste(img, mask=mask)
    return result

def make_ship_image(av1: Image.Image, av2: Image.Image, percent: int, tier: dict) -> io.BytesIO:
    bg_path = ASSETS_PATH / tier["bg_file"]

    if bg_path.exists():
        bg = Image.open(bg_path).convert("RGBA")
        W_orig, H_orig = bg.size
        bg = bg.resize((W_orig * SCALE, H_orig * SCALE), Image.LANCZOS)
    else:
        bg = Image.new("RGBA", (520 * SCALE, 210 * SCALE), (45, 90, 45, 255))

    W, H = bg.size
    S = SCALE
    draw = ImageDraw.Draw(bg, "RGBA")

    bg.paste(av1, (AV_LEFT[0] * S, AV_LEFT[1] * S), av1)
    bg.paste(av2, (AV_RIGHT[0] * S, AV_RIGHT[1] * S), av2)

    pad = 30 * S
    bar_h = 32 * S
    bar_y = H - pad - bar_h
    bar_x = pad
    bar_w = W - pad * 2
    fill_w = int((percent / 100) * bar_w)
    border = 3 * S

    draw.rounded_rectangle(
        (bar_x - border, bar_y - border, bar_x + bar_w + border, bar_y + bar_h + border),
        radius=16 * S, fill=(255, 255, 255, 255)
    )
    draw.rounded_rectangle((bar_x, bar_y, bar_x + bar_w, bar_y + bar_h),
                            radius=14 * S, fill=(20, 20, 20, 210))
    if fill_w > 0:
        draw.rounded_rectangle((bar_x, bar_y, bar_x + fill_w, bar_y + bar_h),
                                radius=14 * S, fill=tier["bar"] + (255,))

    try:
        font = ImageFont.truetype(str(FONT_PATH), 26 * S)
    except Exception:
        font = ImageFont.load_default()

    draw.text((W // 2 + S, bar_y + bar_h // 2 + S), f"{percent}%",
              font=font, anchor="mm", fill=(0, 0, 0, 180))
    draw.text((W // 2, bar_y + bar_h // 2), f"{percent}%",
              font=font, anchor="mm", fill=(255, 255, 255, 255))

    bg = bg.resize((W // S, H // S), Image.LANCZOS)

    output = io.BytesIO()
    bg.convert("RGB").save(output, format="PNG", optimize=True)
    output.seek(0)
    return output


class Ship(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.hybrid_command(name="ship", description="Shippa duas pessoas")
    @app_commands.allowed_installs(users=True, guilds=True)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.describe(
        user1="Primeiro usuário",
        user2="Segundo usuário (se vazio, usa você mesmo)"
    )
    async def ship(
        self,
        ctx: commands.Context,
        user1: discord.User,
        user2: discord.User = None,
    ):
        await ctx.defer()

        if user2 is None:
            user2 = ctx.author

        percent = get_percent(user1.id, user2.id)
        tier_idx = next(i for i, t in enumerate(TIERS) if t["range"][0] <= percent <= t["range"][1])
        tier = TIERS[tier_idx]
        ship_name = get_ship_name(user1.display_name, user2.display_name)
        message = random.choice(tier["messages"])

        av1_url = user1.display_avatar.with_format("png").with_size(512).url
        av2_url = user2.display_avatar.with_format("png").with_size(512).url

        async with aiohttp.ClientSession() as session:
            av1 = await fetch_avatar(session, av1_url)
            av2 = await fetch_avatar(session, av2_url)

        loop = asyncio.get_event_loop()
        img_bytes = await loop.run_in_executor(None, make_ship_image, av1, av2, percent, tier)

        embed = discord.Embed(
            description=(
                f"💞 **{user1.display_name}** + **{user2.display_name}** = ✨ **{ship_name}** ✨\n"
                f"{message}"
            ),
            color=discord.Color.from_rgb(*tier["bar"])
        )
        embed.set_image(url="attachment://ship.png")

        file = discord.File(img_bytes, filename="ship.png")
        await ctx.send(embed=embed, file=file)


async def setup(client: commands.Bot):
    await client.add_cog(Ship(client))