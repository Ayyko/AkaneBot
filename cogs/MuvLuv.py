import discord
from discord.ext import commands
import aiohttp
import asyncio
from .utils.helpers import TimeParser
from .utils import checks

class MuvLuv:
    def __init__(self, bot):
        self.bot = bot
        self.ml_server = "169056767219597312"
        self.ml_announce = self.bot.get_channel("235502028930023424")

    @commands.command(pass_context=True)
    @checks.has_perm("kick_members")
    async def mute(self, ctx, target: discord.Member, time: TimeParser=0, *, reason=""):
        if ctx.message.server.id != self.ml_server:
            return
        if time.seconds < 1:
            self.bot.reply("Please use a valid time")
            return
        mute_role = discord.utils.get(ctx.message.server.roles, id="203241764260151296")
        await self.bot.add_roles(target, mute_role)
        ret = " | Reason: " + reason if reason else ""
        await self.bot.send_message(self.ml_announce, "athere {} muted {} for {} seconds".format(ctx.message.author.mention, target.mention, time.seconds) + ret)

        await asyncio.sleep(time.seconds)
        await self.bot.remove_roles(target, mute_role)
        await self.bot.send_message(self.ml_announce, "{} has been unmuted".format(target.mention))

    async def on_member_join(self, member):
        if member.server.id == self.ml_server:
            await self.bot.send_message(self.ml_announce, "@here Member joined: {a.name}, {a.mention}".format(a=member))

    async def on_member_remove(self, member):
        if member.server.id == self.ml_server:
            await self.bot.send_message(self.ml_announce, "Member left: {a.name}, ({a.id})".format(a=member))

    async def on_member_ban(self, member):
        if member.server.id == self.ml_server:
            await self.bot.send_message(self.ml_announce, "🔨🔨 Member banned: {a.name}, ({a.id}) 🔨🔨".format(a=member))

    async def on_member_unban(self, server, user):
        if server.id == self.ml_server:
            await self.bot.send_message(self.ml_announce, "Member unbanned: {a.name}, ({a.id})".format(a=user))

    async def on_message_edit(self, before, after):
        if before.server.id != self.ml_server:
            return
        if before.content == after.content:
            return
        if before.channel == self.ml_announce:
            return
        ret = "-{}\n+{}".format(before.clean_content, after.clean_content)
        if len(ret) > 1850:
            async with aiohttp.ClientSession() as session:
                async with session.post("http://hastebin.com/documents", data=ret) as r:
                    resp = await r.json()
                    try:
                        hb_url = "http://hastebin.com/{}".format(resp["key"])
                    except KeyError:
                        hb_url = "There was an error uploading to hb: {}".format(resp)
            await self.bot.send_message(self.ml_announce, "{} in #{} edited a pretty big message, hastebin link: {}".format(str(after.author), after.channel.name, hb_url))
            return
        await self.bot.send_message(self.ml_announce, "{} in #{} edited a message:\n ```diff\n{}```".format(str(after.author), after.channel.name, ret))

    async def on_message_delete(self, message):
        if message.server.id != self.ml_server:
            return
        if message.channel == self.ml_announce:
            return
        if len(message.clean_content) > 1900:
            async with aiohttp.ClientSession() as session:
                async with session.post("http://hastebin.com/documents", data=message.clean_content) as r:
                    resp = await r.json()
                    try:
                        hb_url = "http://hastebin.com/{}".format(resp["key"])
                    except KeyError:
                        hb_url = "There was an error uploading to hb: {}".format(resp)
            await self.bot.send_message(self.ml_announce, "{} in #{} deleted a pretty big message, hastebin link: {}".format(str(message.author), message.channel.name, hb_url))
            return
        await self.bot.send_message(self.ml_announce, "{} in #{} deleted a message:\n```{}```".format(str(message.author), message.channel.name, message.clean_content))


def setup(bot):
    bot.add_cog(MuvLuv(bot))
