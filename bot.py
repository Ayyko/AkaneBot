import discord
from discord.ext import commands
import json
import logging
import sys
import asyncio
import cogs
import traceback

# logger = logging.getLogger('discord')
# logger.setLevel(logging.DEBUG)
# handler = logging.StreamHandler(stream=sys.stdout)
# logger.addHandler(handler)

description = '''A bot made for stuff and things.
It can probably do said stuff, potentially even things.
Check out the source at https://github.com/Ayyko/AkaneBot
Made by Ako using discord.py version ''' + discord.__version__

startup_extensions = ["cogs.MuvLuv", "cogs.owner", "cogs.search", "cogs.repl", "cogs.utility"]

async def get_pre(self, message):
    ret = [commands.when_mentioned(self, message), "Akane ", "akane ", "(•ω•) "]
    if message.guild and message.guild.id == 169056767219597312:
        ret += ["ml ", "Ml ", "ML ", "mL "]
    if message.author.id == 132694825454665728:  # Me
        ret += ["baka ", "bakane "]
    return ret

bot = commands.Bot(command_prefix=get_pre, description=description, pm_help=True)

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


with open("bot_shit.json", "r") as b:
    bot.shit = json.load(b)


bot.run(bot.shit['token'])
