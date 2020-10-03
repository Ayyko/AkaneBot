import discord
from discord.ext import commands
import json
import logging
import sys
import cogs
import traceback
import aiohttp
import urllib

# logger = logging.getLogger('discord')
# logger.setLevel(logging.DEBUG)
# handler = logging.StreamHandler(stream=sys.stdout)
# logger.addHandler(handler)

description = '''A bot made for stuff and things.
It can probably do said stuff, potentially even things.
Check out the source at https://github.com/Ayyko/AkaneBot
Made by Ako#0408(132694825454665728) using discord.py version ''' + discord.__version__

startup_extensions = ["cogs.MuvLuv", "cogs.owner", "cogs.search", "cogs.utility", "cogs.nsa", "cogs.animanga"]

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix=["Akane ", "akane ", "<@202989516904988673> ", "<@!202989516904988673> "], description=description, pm_help=True, intents=intents)


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))
            traceback.print_exc()


@bot.command()
@commands.cooldown(1, 60, commands.cooldowns.BucketType.channel)
async def about(ctx):
    """Information about the bot (same as shown at the top of help)"""
    await ctx.send(description)


with open("bot_shit.json", "r") as b:
    bot.shit = json.load(b)


# @bot.event
# async def on_message(message):
#
#     await bot.process_commands(message)

bot.run(bot.shit['token'])

with open("bot_shit.json", "w") as b:
    a = json.dumps(bot.shit)
    b.write(a)
