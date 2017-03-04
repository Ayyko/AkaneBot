import discord
from discord.ext import commands
import aiohttp
import asyncio
from .utils.helpers import TimeParser
from .utils import checks


class MuvLuv:
    def __init__(self, bot):
        self.bot = bot
        self.ml_guild = 169056767219597312
        self.ml_announce = self.bot.get_channel(235502028930023424)

    @commands.command()
    @checks.has_perm("kick_members")
    async def mute(self, ctx, target: discord.Member, time: TimeParser=0, *, reason=""):
        """Mutes a member for [time], with an optional reason"""
        if ctx.guild.id != self.ml_guild:
            return
        if time.seconds < 1:
            self.bot.reply("Please use a valid time")
            return
        mute_role = discord.utils.get(ctx.guild.roles, id=203241764260151296)
        await self.bot.add_roles(target, mute_role)
        ret = " | Reason: " + reason if reason else ""
        await self.ml_announce.send("@here {} muted {} for {} seconds".format(ctx.message.author.mention, target.mention, time.seconds) + ret)

        await asyncio.sleep(time.seconds)
        await self.bot.remove_roles(target, mute_role)
        await self.ml_announce.send_message(self.ml_announce, "{} has been unmuted".format(target.mention))

    async def on_member_join(self, member):
        if member.guild.id == self.ml_guild:
            await self.ml_announce.send("@here Member joined: {a.name}, {a.mention}".format(a=member))

    async def on_member_remove(self, member):
        if member.guild.id == self.ml_guild:
            await self.ml_announce.send("Member left: {a.name}, ({a.id})".format(a=member))

    async def on_member_ban(self, member):
        if member.guild.id == self.ml_guild:
            await self.ml_announce.send("🔨🔨 Member banned: {a.name}, ({a.id}) 🔨🔨".format(a=member))

    async def on_member_unban(self, guild, user):
        if guild.id == self.ml_guild:
            await self.ml_announce.send("Member unbanned: {a.name}, ({a.id})".format(a=user))

    async def on_message_edit(self, before, after):
        if before.guild.id != self.ml_guild:
            return
        if before.content == after.content:
            return
        if before.channel == self.ml_announce:
            return
        ret = "-{}\n+{}".format(before.clean_content, after.clean_content)
        if len(ret) > 1850:
            async with aiohttp.ClientSession() as session:
                async with session.post("https://hastebin.com/documents", data=ret) as r:
                    resp = await r.json()
                    try:
                        hb_url = "https://hastebin.com/{}".format(resp["key"])
                    except KeyError:
                        hb_url = "There was an error uploading to hb: {}".format(resp)
            await self.ml_announce.send("{} in #{} edited a pretty big message, hastebin link: {}".format(str(after.author), after.channel.name, hb_url))
            return
        await self.ml_announce.send("{} in #{} edited a message:\n ```diff\n{}```".format(str(after.author), after.channel.name, ret))

    async def on_message_delete(self, message):
        if message.guild.id != self.ml_guild:
            return
        if message.channel == self.ml_announce:
            return
        if len(message.clean_content) > 1900:
            async with aiohttp.ClientSession() as session:
                async with session.post("https://hastebin.com/documents", data=message.clean_content) as r:
                    resp = await r.json()
                    try:
                        hb_url = "https://hastebin.com/{}".format(resp["key"])
                    except KeyError:
                        hb_url = "There was an error uploading to hb: {}".format(resp)
            await self.ml_announce.send("{} in #{} deleted a pretty big message, hastebin link: {}".format(str(message.author), message.channel.name, hb_url))
            return
        await self.ml_announce.send("{} in #{} deleted a message:\n```{}```".format(str(message.author), message.channel.name, message.clean_content))


def setup(bot):
    bot.add_cog(MuvLuv(bot))
