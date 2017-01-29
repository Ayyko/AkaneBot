from discord.ext import commands
from cogs.utils import checks
import discord
from PIL import Image
import aiohttp
import io

class Utility:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def whois(self, ctx, target: discord.Member=None):
        target = target or ctx.message.author
        roles = ", ".join([r.name.replace('@', '@\u200b') for r in target.roles])
        default = False
        if target.avatar:
            url = target.avatar_url
        else:
            url = target.default_avatar_url
            default = True
        with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                idk = await resp.read()
                img = Image.open(io.BytesIO(idk)).convert("RGB")
                # print(img.getcolors(img.size[0] * img.size[1]))
                # print(sorted(img.getcolors(img.size[0] * img.size[1]), key=lambda m: m[0])[::-1])
                colors = sorted(img.getcolors(img.size[0] * img.size[1]), key=lambda m: m[0])[::-1]
                color = colors[not default][1]
                for c in colors:
                    if not(180<c[1][0] and 180<c[1][1] and 180<c[1][2]) and not(c[1][0]<50 and c[1][1]<50 and c[1][2]<50):
                        color = c[1]
                        break
                # print(color)
                # print(img.getpixel((0,0)))
                # print(img.getpixel((0,1)))

                colorint = (color[0] * 65536) + (color[1] * 256) + color[2]  # (R*65536)+(G*256)+B



        embed = discord.Embed()
        embed.set_author(name=str(target), icon_url=target.avatar_url if target.avatar else target.default_avatar_url)
        embed.add_field(name="Nickname", value=target.display_name if target.display_name != target.name else "None")
        embed.add_field(name="Status", value=target.status)
        embed.add_field(name="Account Created", value=target.created_at)
        embed.add_field(name="Joined", value=target.joined_at)
        embed.add_field(name="Roles", value=roles)
        embed.color = colorint
        await self.bot.say("", embed=embed)

def setup(bot):
    bot.add_cog(Utility(bot))
