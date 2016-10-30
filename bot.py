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

startup_extensions = ["cogs.MuvLuv", "cogs.owner", "cogs.search"]

async def get_pre(self, message):
    ret = [message.server.me.mention, "Akane ", "akane ", "(•ω•) "]
    if message.server.id == "169056767219597312":
        ret += ["ml ", "Ml ", "ML ", "mL "]
    if message.author.id == "132694825454665728":  # Me
        ret += ["baka "]
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

# MOVED TO muvluv.py
# @bot.event
# async def on_member_join(member):
#     if not member.server.id == "169056767219597312":
#         return
#     announce = member.server.get_channel("198237266202591232")
#     await bot.send_message(announce, "@here We have a new member: " + member.name + " (id: " + member.id + ")")


# WTF?
# @bot.event
# async def on_message(message):
#     save()
#     await bot.process_commands(message)


# MOVED TO /utils/checks.py
# def is_owner():
#     return commands.check(lambda ctx: ctx.message.author.id == "132694825454665728")


# MOVED TO owner.py
# @bot.command(pass_context=True, hidden=True)
# @is_owner()
# async def debug(ctx, *, code: str):
#     """Extremely unsafe eval command."""
#     code = code.strip("` ")
#     python = "```python\n{0}\n```"
#     result = None
#
#     try:
#         result = eval(code)
#     except Exception as error:
#         await bot.say(python.format(type(error).__name__ + ': ' + str(error)))
#         return
#
#     if asyncio.iscoroutine(result):
#         result = await result
#
#     await bot.say(python.format(result))


# MOVED TO owner.py
# @bot.command(pass_context=True, hidden=True)
# @is_owner()
# async def die(ctx, hidden=True):
#     await bot.say("Bye-bye")
#     await bot.logout()


# Gotta move this to a task or something not as stupid
# def save():
#     if bot.shit is not "":
#         with open("bot_shit.json", "w") as c:
#             json.dump(bot.shit, c)


with open("bot_shit.json", "r") as b:
    bot.shit = json.load(b)


bot.run(bot.shit['token'])
