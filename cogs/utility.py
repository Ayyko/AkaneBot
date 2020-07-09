from discord.ext import commands
import discord
import datetime
import aiohttp
import io
import random
import typing



class GenObj(commands.Converter):
    async def convert(self, ctx, argument):
        return argument.id


class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["choose", "choice"])
    async def flip(self, ctx, arg1: str, arg2: str, *, args=None):
        choices = [arg1, arg2]
        if args:
            choices.extend(args.split())
        choice = random.choice(choices)
        await ctx.send(choice.replace("@", "@​​\u200B"))

    @commands.command()
    async def age(self, ctx, id: typing.Union[int, GenObj]):
        """Finds the age relative to the current time of any id or discord Object"""
        create_delta = datetime.datetime.utcnow() - discord.utils.snowflake_time(id)
        create_list = ["today", "a day ago", "two days ago", "a few days ago", "a few days ago", "a few days ago", "a few days ago", "a week ago", "a week ago", "a week ago"]
        create_str = "a while ago " if create_delta.days > 9 else create_list[create_delta.days]
        await ctx.send("Created {b} [{c} ago]".format(b=create_str, c=str(create_delta)))
        

def setup(bot):
    bot.add_cog(Utility(bot))
