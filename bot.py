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


description = '''A bot made for the Muv Luv Fans server

Made by Ako using discord.py'''

startup_extensions = ["cogs.tags", "cogs.roles"]

bot = commands.Bot(command_prefix=['ml ', 'ML ', 'Ml ', 'mL ', 'akane', 'Akane', '<@202989516904988673> ', '<@!202989516904988673> '], description=description, pm_help=True)


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

@bot.event
async def on_member_join(member):
    if not member.server.id == "169056767219597312":
        return
    announce = member.server.get_channel("198237266202591232")
    await bot.send_message(announce, "@here We have a new member: " + member.name + " (id: " + member.id + ")")


@bot.event
async def on_message(message):
    save()
    bot.process_commands


def is_owner():
    return commands.check(lambda ctx: ctx.message.author.id == "132694825454665728")


@bot.command(pass_context=True, hidden=True)
@is_owner()
async def debug(ctx, *, code: str):
    """Extremely unsafe eval command."""
    code = code.strip("` ")
    python = "```python\n{0}\n```"
    result = None

    try:
        result = eval(code)
    except Exception as error:
        await bot.say(python.format(type(error).__name__ + ': ' + str(error)))
        return

    if asyncio.iscoroutine(result):
        result = await result

    await bot.say(python.format(result))


@bot.command(pass_context=True, hidden=True)
@is_owner()
async def die(ctx, hidden=True):
    await bot.say("Bye-bye")
    bot.logout


def save():
    if bot.shit is not "":
        with open("bot_shit.json", "w") as c:
            json.dump(bot.shit, c)


with open("bot_shit.json", "r") as b:
    bot.shit = json.load(b)


bot.run(bot.shit['token'])
