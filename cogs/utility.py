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

    @commands.command()
    async def votekick(self, ctx, target: discord.Member):
        if ctx.guild.id != 203903748597219328:  # personal server
            return
        if not target:
            await ctx.send("pick a real person (mention them if you have to)")
            return
        if target.id not in self.bot.shit["votes"]["kick"]:
            self.bot.shit["votes"]["kick"][target.id] = [ctx.message.author.id]
        else:
            if ctx.message.author.id in self.bot.shit["votes"]["kick"]:
                self.bot.shit["votes"]["kick"][target.id].remove(ctx.message.author.id)
                await ctx.send("Your vote has been removed")
            else:
                self.bot.shit["votes"]["kick"][target.id].append(ctx.message.author.id)
        await ctx.send("There are now {} votes out of 5 needed to kick {}".format(len(self.bot.shit["votes"]["kick"][target.id]), target))
        if len(self.bot.shit["votes"]["kick"][target.id]) > 4:
            await ctx.guild.kick(target)
            await ctx.send("{} has been kicked by popular vote".format(target))
            ret = "The members who voted for this were "
            for voter in self.bot.shit["votes"]["kick"][target.id]:
                ret += "<@{}> ".format(str(voter))
            await ctx.send(ret)
            del self.bot.shit["votes"]["kick"][target.id]

    @commands.command()
    async def voteban(self, ctx, target: discord.Member):
        if ctx.guild.id != 203903748597219328:  # personal server
            return
        if not target:
            await ctx.send("pick a real person (mention them if you have to)")
            return
        if target.id not in self.bot.shit["votes"]["ban"]:
            self.bot.shit["votes"]["ban"][target.id] = [ctx.message.author.id]
        else:
            if ctx.message.author.id in self.bot.shit["votes"]["ban"][target.id]:
                self.bot.shit["votes"]["ban"][target.id].remove(ctx.message.author.id)
                await ctx.send("Your vote has been removed")
            else:
                self.bot.shit["votes"]["ban"][target.id].append(ctx.message.author.id)
        await ctx.send("There are now {} votes out of 7 needed to ban {}".format(len(self.bot.shit["votes"]["ban"][target.id]), target))
        if len(self.bot.shit["votes"]["ban"][target.id]) > 6:
            await ctx.guild.ban(target)
            await ctx.send("{} has been banned by popular vote".format(target))
            ret = "The members who voted for this were "
            for voter in self.bot.shit["votes"]["ban"][target.id]:
                ret += "<@{}> ".format(str(voter))
            await ctx.send(ret)
            del self.bot.shit["votes"]["ban"][target.id]


def setup(bot):
    bot.add_cog(Utility(bot))
