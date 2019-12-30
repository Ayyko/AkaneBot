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

startup_extensions = ["cogs.MuvLuv", "cogs.owner", "cogs.search", "cogs.utility", "cogs.twitter", "cogs.nsa"]

# async def get_pre(self, message):
#     ret = commands.when_mentioned(self, message)
#     ret += ["Akane ", "akane ", "(•ω•) "]
#     if message.guild and message.guild.id == 169056767219597312:
#         ret += ["ml ", "Ml ", "ML ", "mL "]
#     if message.author.id == 132694825454665728:  # Me
#         ret += ["baka ", "bakane "]
#     return ret

bot = commands.Bot(command_prefix=["Akane ", "akane ", "<@202989516904988673> ", "<@!202989516904988673> "], description=description, pm_help=True)


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


@bot.event
async def on_message(message):
    if message.guild.id in bot.shit['anime_guilds'] and message.content.startswith("{{")\
            and message.content.endswith("}}"):
        if message.content[2:-2] in bot.shit["anime_syns"]:
            title = urllib.parse.quote(bot.shit["anime_syns"][message.content[2:-2]])
        else:
            title = urllib.parse.quote(message.content[2:-2])
        base_url = "https://api.jikan.moe/v3/search/anime?q="
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(base_url+title) as resp:
                    if resp.status == 200:
                        results = await resp.json()
                    else:
                        await message.channel.send("Something went wrong.")
                        print(resp)
                        return
            if "results" in results and results["results"]:
                await message.channel.send("<" + results["results"][0]["url"] + ">")
            else:
                await message.channel.send("Anime not found.")
        except Exception as e:
            await message.channel.send("Something went wrong. Error: " + e)

    await bot.process_commands(message)


@bot.command(name="add syn", aliases=["add synonym", "add anime", "aadd", "addanime"])
async def add_syn(ctx, syn, *, anime):
    bot.shit["anime_syns"][syn] = anime
    await ctx.send("Synonym added")


bot.run(bot.shit['token'])

with open("bot_shit.json", "w") as b:
    a = json.dumps(bot.shit)
    b.write(a)
