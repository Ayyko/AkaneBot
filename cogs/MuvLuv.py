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
        self.ml_invite = "https://discord.gg/Zu9Dp2s"
        self.auto_kicks = {}

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
        await self.ml_announce.send("{} has been unmuted".format(target.mention))

    async def on_member_join(self, member):
        if member.guild.id == self.ml_guild:
            await self.ml_announce.send("@here Member joined: {a.name}, {a.mention}".format(a=member))

            # Auto Modding stuff

            if member.bot:
                return
            if str(member.id) in self.auto_kicks and self.auto_kicks[str(member.id)]:
                await member.add_roles(*self.auto_kicks[str(member.id)])

    async def on_member_remove(self, member):
        if member.guild.id == self.ml_guild:
            await self.ml_announce.send("Member left: {a.name}, ({a.id})".format(a=member))

    async def on_member_ban(self, guild, member):
        if guild.id == self.ml_guild:
            await self.ml_announce.send("🔨🔨 Member banned: {a.name}, ({a.id}) 🔨🔨".format(a=member))

        # DAPI stuff for abal
        if guild.id == 81384788765712384:
            await asyncio.sleep(3)  # whatever time idk
            async for entry in guild.audit_logs(limit=3, action=discord.AuditLogAction.ban):
                if entry.target.id != member.id:
                    continue
                else:
                    print('{0.user} banned {0.target}'.format(entry))

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
            await self.ml_announce.send("{} in #{} edited a pretty big message, hastebin link: {}.diff".format(str(after.author), after.channel.name, hb_url))
            return
        await self.ml_announce.send("{} in #{} edited a message:\n ```diff\n{}```".format(str(after.author), after.channel.name, ret))

    async def on_message_delete(self, message):
        if message.guild.id != self.ml_guild:
            return
        if message.channel == self.ml_announce:
            return
        await asyncio.sleep(3)
        deleter = None
        async for entry in message.guild.audit_logs(limit=3, action=discord.AuditLogAction.message_delete):
            if message.author.id != entry.target.id:
                continue
            else:
                deleter = entry.user.id
        #audit log check: if none then self delete(or bot), else get deleter
        if len(message.clean_content) > 1900:
            async with aiohttp.ClientSession() as session:
                async with session.post("https://hastebin.com/documents", data=message.clean_content) as r:
                    resp = await r.json()
                    try:
                        hb_url = "https://hastebin.com/{}".format(resp["key"])
                    except KeyError:
                        hb_url = "There was an error uploading to hb: {}".format(resp)
            if deleter:
                await self.ml_announce.send("in #{} a pretty big message by {} was deleted by {}, hastebin link: {}".format(message.channel.name, str(message.author), str(message.guild.get_member(deleter)), hb_url))
                return
            await self.ml_announce.send("{} in #{} deleted a pretty big message, hastebin link: {}".format(str(message.author), message.channel.name, hb_url))
            return
        if deleter:
            await self.ml_announce.send("in #{} a message by {} was deleted by {}:\n```{}```".format(message.channel.name, str(message.author), str(message.guild.get_member(deleter)), message.clean_content))
            return
        await self.ml_announce.send("{} in #{} deleted a message:\n```{}```".format(str(message.author), message.channel.name, message.clean_content))

    # anti raid/auto modding stuff

    async def on_message(self, message):
        if not message.guild or message.guild.id != self.ml_guild:
            return
        if message.author.bot:
            return
        if message.embeds and message.embeds[0].type == "rich" and self.is_embed_massive(message.embeds[0]):
            await message.author.ban()
            await self.ml_announce.send("@everyone I automatically banned a user {0} ({0.id}) for sending a large embed".format(message.author))
        if message.mentions and len(message.mentions) > 10:
            await message.delete()
            self.auto_kicks[str(message.author.id)] = message.author.roles
            await message.author.send("Hi, I have automatically kicked you from the Muv-Luv Fans server for having more than 10 mentions in a single message.\nThis is an anti-spam "
                                      "measure and was preformed automatically, please join back if this was not malicious.\n{}".format(self.ml_invite))  # I have to send this before the kick to share a server with them.
            await message.author.kick()

            await self.ml_announce.send("@here I automatically kicked a user {0} ({0.id}) for sending a message with over 10 mentions".format(message.author))

    def is_embed_massive(self, embed):
        embed_size = len(embed.description) if embed.description else 0
        for field in embed.fields:
            embed_size += len(field.value)
        return embed_size > 3000


def setup(bot):
    bot.add_cog(MuvLuv(bot))
