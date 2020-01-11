from discord.ext import commands
import discord
from PIL import Image
import aiohttp
import io
import random


class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["who is"])
    async def whois(self, ctx, *, target: discord.Member=None):
        """Returns information about a user"""
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
                    if not(180 < c[1][0] and 180 < c[1][1] and 180 < c[1][2]) and not(c[1][0] < 50 and c[1][1] < 50 and c[1][2] < 50):
                        color = c[1]
                        break
                # print(color)
                # print(img.getpixel((0,0)))
                # print(img.getpixel((0,1)))

                colorint = (color[0] * 65536) + (color[1] * 256) + color[2]  # (R*65536)+(G*256)+B

        embed = discord.Embed()
        embed.set_author(name=str(target), icon_url=target.avatar_url if target.avatar else target.default_avatar_url)
        embed.add_field(name="ID", value=str(target.id))
        embed.add_field(name="Nickname", value=target.display_name if target.display_name != target.name else "None")
        embed.add_field(name="Status", value=target.status)
        embed.add_field(name="Account Created", value=str(target.created_at)[:22])
        embed.add_field(name="Joined", value=str(target.joined_at)[:22])
        embed.add_field(name="Roles ({})".format(len(target.roles)), value=roles)
        embed.color = colorint
        await ctx.send("", embed=embed)

    @commands.command(aliases=["choose", "choice"])
    async def flip(self, ctx, arg1: str, arg2: str, *, args=None):
        choices = [arg1, arg2]
        if args:
            choices.extend(args.split())
        choice = random.choice(choices)
        await ctx.send(choice.replace("@", "@​​\u200B"))



def setup(bot):
    bot.add_cog(Utility(bot))
