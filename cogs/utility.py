from discord.ext import commands
from cogs.utils import checks
import discord
from PIL import Image
import aiohttp

class Utility:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def whois(self, ctx, target: discord.Member=None):
        target = target or ctx.message.author
        roles = ", ".join([r.name.replace('@', '@\u200b') for r in target.roles])

        with aiohttp.ClientSession() as session:
            async with session.get(target.avatar_url) as resp:
                img = Image.open(resp.read())
                color = sorted(img.getcolors(), key=lambda m: m[0])[0][1]
                colorint = (color[0] * 65536) + (color[1] * 256) + color[2]  # (R*65536)+(G*256)+B

        embed = discord.Embed()
        embed.set_author(str(target), icon_url=target.avatar_url)

        embed.add_field("Nickname", target.display_name if target.display_name != target.name else "None")
        embed.add_field("Status", target.status)
        embed.add_field("Account Created", target.created_at)
        embed.add_field("Joined", target.joined_at)
        embed.add_field("Roles", roles)
        embed.color = colorint

