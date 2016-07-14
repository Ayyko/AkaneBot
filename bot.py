import discord
from discord.ext import commands
import json
import logging
import sys
import asyncio

# logger = logging.getLogger('discord')
# logger.setLevel(logging.DEBUG)
# handler = logging.StreamHandler(stream=sys.stdout)
# logger.addHandler(handler)


description = '''A bot made for the Muv Luv Fans server

Made by Ako using discord.py'''


# Decided not to use channel groups as it was a bit of a hurdle that was setting me back at the time
# Might go back and add it later

# lvl1_chan = ['172471649344421889',  # Extra
#              '172471692981960705',  # Unlimited
#              '172471751328923648',  # Alternative
#              '173088894361927680',  # Schwarzesmarken
#              '173089766584221696',  # Chronicles
#              '173090227840090114',  # Total_Eclipse
#              '173090779579809792',  # Kimi_Ga_Nozomu_Eien
#              '173091276160368640',  # Haruko_Maniax
#              '185873082609696768',  # Alternative_Divergence_Fanficion
#              '173129713320067073',  # Akane_Maniax
#              '174219435844960256',  # Altered_Fable
#              ]
#
# lvl2_chan = ['172471692981960705',  # Unlimited
#              '172471751328923648',  # Alternative
#              '173088894361927680',  # Schwarzesmarken
#              '173089766584221696',  # Chronicles
#              '173090227840090114',  # Total_Eclipse
#              '173090779579809792',  # Kimi_Ga_Nozomu_Eien
#              '173091276160368640',  # Haruko_Maniax
#              '185873082609696768',  # Alternative_Divergence_Fanficion
#              '173129713320067073',  # Akane_Maniax
#              '174219435844960256',  # Altered_Fable
#              ]
#
# lvl3_chan = ['172471751328923648',  # Alternative
#              '173088894361927680',  # Schwarzesmarken
#              '173089766584221696',  # Chronicles
#              '173090227840090114',  # Total_Eclipse
#              '173090779579809792',  # Kimi_Ga_Nozomu_Eien
#              '173091276160368640',  # Haruko_Maniax
#              '185873082609696768',  # Alternative_Divergence_Fanficion
#              '173129713320067073',  # Akane_Maniax
#              '174219435844960256',  # Altered_Fable
#              ]

bot = commands.Bot(command_prefix=['ml ', 'ML ', 'Ml ', 'mL ', 'maburabu ', 'MabuRabu ', '<@196485834273193985> ', '<@!196485834273193985> '], description=description, pm_help=True)


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.event
async def on_member_join(member):
    if not member.server.id == "169056767219597312":
        return
    announce = member.server.get_channel("198237266202591232")
    await bot.send_message(announce, "@here " + member.name + " (" + member.id + ") new member!")



# Decided to put off tags for now, as I feel like they might be a bit too meme-y for this server. might experiment with

# @bot.group(name="tags", pass_context=True, no_pm=True)
# async def tag(ctx):
#     """Lists all tags that can be used in the current channel
#
#         Usage: `tags`
#         New tags can be added with the `tag add` command.
#         A list of all tags can be received in pm by using the `tag all` command. (watch out for possible spoilers in the tag names)
#         A list of a specific channel's tag list can be received in pm by using the 'tag channel [#channel_name]' command"""
#     ret = ""
#     if ctx.message.channel.id in bot_shit['tags'] and bot_shit['tags'][ctx.message.channel.id]:
#         ret += "Channel specific tags:\n" + ", ".join(bot_shit['tags'][ctx.message.channel.id]) + "\n"
#     ret += "Global tags:\n" + ", ".join(bot_shit['tags']["global"])
#     await bot.say(ret)
#
#
# @tag.command(pass_context=True, no_pm=True)
# async def create(ctx, name, *, tag_content):
#     """Create a new channel specific tag.
#
#     Usage: `tag create [name] [content]`
#     By default the new tag is only accessible in the channel it was made.
#     To create a tag for use in any channel, use the `tag server` command
#     """
#     if name in bot.commands:
#         await bot.say("Sorry, {} is the name of one of the bots commands, choose another".format(name))
#         return
#
#     if name in bot_shit['tags'][ctx.message.channel.id]:
#         await bot.say("A tag with this name already exists in this channel")
#         return
#
#     if name in bot_shit['tags']['global']:
#         await bot.say("A server tag with that name already exists")
#         return
#
#     bot_shit['tags'][ctx.message.channel.id][name] = {"content": tag_content, "owner": ctx.message.author.id}
#     await bot.say("Tag {} created successfully for use in this channel".format(name))
#     save()
#
#
# @tag.command(pass_context=True)
# async def server(ctx, name, *, tag_content):
#     """Create a new server tag, usable in any channel.
#
#     Usage: `tag server [name] [content]`
#     For any possible spoiler, please use the `tag create` command instead, to prevent spoilers from leaving their relevant channels.
#     Misuse of server tags will be severely punished, constant misuse may result in it being only usable by certain members"""
#     if name in bot.commands:
#         await bot.say("Sorry, {} is the name of one of the bots commands, choose another".format(name))
#         return
#
#     if name in bot_shit['tags']['global']:
#         await bot.say("A server tag with that name already exists")
#         return
#
#     for chan in bot_shit['tags']:
#         if name in bot_shit['tags'][chan]:
#             await bot.say("A tag with this name has already been made for the {}.name channel".format(bot.get_channel(chan)))
#             return
#
#     bot_shit['tags']['global'][name] = {"content": tag_content, "owner": ctx.message.author.id}
#     await bot.say("Sever tag {} created successfully".format(name))
#     save()
#
#
# @tag.command(pass_context=True, no_pm=True)
# async def remove(ctx, name):
#     """Remove a tag by name.
#
#     Usage `tag remove [name]`
#     Attempts to remove Channel specific tag from the channel of the message before moving on to checking server-wide tags
#     Tag owners and Mods are the only ones allowed to remove tags"""
#     if any([n == name for n in bot_shit['tags'][ctx.message.channel.id]]):
#         if any([r.permissions.manage_messages for r in ctx.message.author.roles]) or bot_shit['tags'][ctx.message.channel.id][name]['owner'] == ctx.message.author.id:
#             del bot_shit['tags'][ctx.message.channel.id][name]
#             await bot.say("Channel specific tag {} has been removed".format(name))
#             return
#         await bot.say("Only the owner or a mod can remove tags")
#
#     elif any([n == name for n in bot_shit['tags']['global']]):
#         if any([r.permissions.manage_messages for r in ctx.message.author.roles]) or bot_shit['tags']['global'][name]['owner'] == ctx.message.author.id:
#             del bot_shit['tags']['global'][name]
#             await bot.say("Server tag {} has been removed".format(name))
#             return
#         await bot.say("Only the owner or a mod can remove tags")
#
#     else:
#         await bot.say("No tag with that name exists")

@bot.group(pass_context=True)
async def roles(ctx):
    """Displays basic info about roles and channels

    Usage: `roles`
    If this outdated just mention it to Ako"""
    if "role_msg" not in bot_shit or bot_shit['role_msg'] is "":
        bot_shit['role_msg'] = "This is a (hopefully) current list of assignable roles and their meaning:\n" \
                               "```Cadet: For those currently reading/planning to soon read Muv-Luv\n" \
                               "Recruit: For those who have completed (or want to see spoilers for) Extra and Unlimited but not Alternative\n" \
                               "Eishi: For those who have completed (or want to see spoilers for) Extra, Unlimited and Alternative\n" \
                               "Valkyrie Member: For those who have completed (or want to see spoilers for) All Muv-Luv related content, including other VNs and shows\n" \
                               "Spoiler Reader: Allows access to the message history of <#179284511803179008> and <#179284770210054145>. Be warned: These channels can have spoilers for anything at any time\n" \
                               "Muv Luv Alternative Divergence: Allows access to the channel for theglob1981's fanfic (Main Trilogy spoilers)```\n" \
                               "These roles can be given using the `roles add [name]` command"
    await bot.whisper(bot_shit['role_msg'])
    await bot.say(ctx.message.author.mention + ", check your PMs", delete_after=10)

@roles.command(pass_context=True, no_pm=True)
async def add(ctx, *, role: str):
    """Add a role from the list mentioned in the `roles` command

    Currently accepted role names (case-insensitive):
    Cadet, Recruit, Eishi, Valkyrie, Valkyrie Member, Spoiler, Spoiler Reader, Muv Luv Alternative Divergence, Divergence, Alternative Divergence, Fanfic, MLAD
    Please note roles currently cannot be removed via the bot, so choose wisely, and mute potential spoiler channels you don't wish to read"""
    cadet = discord.utils.get(ctx.message.server.roles, id="188030091148656641")
    recruit = discord.utils.get(ctx.message.server.roles, id="173104384392167425")
    eishi = discord.utils.get(ctx.message.server.roles, id="173100677793316865")
    valkyrie = discord.utils.get(ctx.message.server.roles, id="173100534474080257")
    spoiler = discord.utils.get(ctx.message.server.roles, id="180756419174203393")
    mlad = discord.utils.get(ctx.message.server.roles, id="185872382886412297")
    if role[0].lower() == "cadet":
        await bot.add_roles(ctx.message.author, cadet)
        return
    if role[0].lower() == "recruit":
        await bot.add_roles(ctx.message.author, cadet, recruit)
        return
    if role[0].lower() == "eishi":
        await bot.add_roles(ctx.message.author, cadet, recruit, eishi)
    if role[0].lower() == "valkyrie":
        await bot.add_roles(ctx.message.author, cadet, recruit, eishi, valkyrie)
        return
    if role[0].lower() == "spoiler":
        await bot.add_roles(ctx.message.author, spoiler)
        return
    if role[0].lower() == "mlad" or role[0].lower() == "fanfic" or role[0].lower() == "divergence" or "alternative" in [x.lower() for x in role] and "divergence" in [x.lower() for x in role]:
        await bot.add_roles(ctx.message.author, mlad)


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


@bot.command(pass_context=True, hidden=False)
@is_owner()
async def die(ctx):
    bot.say("Bye-bye")
    await bot.logout


def save():
    with open("bot_shit.json", "w") as c:
        c.write(json.dump(bot_shit))


with open("bot_shit.json", "r") as b:
    bot_shit = json.load(b)


bot.run(bot_shit['token'])
