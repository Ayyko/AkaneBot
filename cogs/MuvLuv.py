import discord
from discord.ext import commands
import aiohttp
import asyncio
import datetime
from .utils.helpers import TimeParser
from .utils.checks import has_perm


class MuvLuv(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ml_guild = 169056767219597312
        self.ml_announce = self.bot.get_channel(235502028930023424)
        self.ml_invite = "https://discord.gg/8J7ANjx"
        self.ml_roles = {358065563164999690: [discord.Object(id=188030091148656641)],        # cadet
                         358066129345708032: [discord.Object(id=173104384392167425),
                                              discord.Object(id=188030091148656641)],  # eishi
                         358066125696794624: [discord.Object(id=173100534474080257),
                                              discord.Object(id=173104384392167425),
                                              discord.Object(id=188030091148656641)],  # valk
                         593245068702253076: [discord.Object(id=360896131015639042)],    # lewd
                         593245318888292383: [discord.Object(id=180756419174203393)]}    # spoiler

    @commands.command(enabled=False)
    @has_perm("kick_members")
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

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.guild.id != self.ml_guild:
            return
        create_delta = datetime.datetime.utcnow() - discord.utils.snowflake_time(member.id)
        create_list = ["today", "a day ago", "two days ago", "a few days ago", "a few days ago", "a few days ago", "a few days ago", "a week ago", "a week ago", "a week ago"]
        create_str = "a while ago" if create_delta.days > 9 else create_list[create_delta.days]
        
        await self.ml_announce.send("@here Member joined: {a.name} [{a.mention}] created {b} [{c} ago]".format(a=member, b=create_str, c=str(create_delta)))

        if member.bot:
            return
        await member.add_roles(discord.utils.get(member.guild.roles, id=588420756208353291))

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if member.guild.id != self.ml_guild:
            return
        await self.ml_announce.send("Member left: {a.name}, ({a.id})".format(a=member))

    @commands.Cog.listener()
    async def on_member_ban(self, guild, member):
        if guild.id != self.ml_guild:
            return
        await self.ml_announce.send("🔨🔨 Member banned: {a.name}, ({a.id}) 🔨🔨".format(a=member))

    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        if guild.id != self.ml_guild:
            return
        await self.ml_announce.send("Member unbanned: {a.name}, ({a.id})".format(a=user))

    @commands.Cog.listener()
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
            await self.ml_announce.send("{} in <#{}> edited a pretty big message, hastebin link: {}.diff".format(str(after.author), after.channel.id, hb_url))
            return
        await self.ml_announce.send("{} in <#{}> edited a message:\n ```diff\n{}```".format(str(after.author), after.channel.id, ret))

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.guild.id != self.ml_guild:
            return
        if message.channel == self.ml_announce:
            return
        await asyncio.sleep(3)
        deleter = None
        async for entry in message.guild.audit_logs(limit=3, action=discord.AuditLogAction.message_delete):
            if abs(datetime.datetime.utcnow().timestamp() - discord.utils.snowflake_time(entry.id).timestamp()) < 8:
                deleter = entry.user.id
        # audit log check: if none then self delete(or bot), else get deleter
        if len(message.clean_content) > 1900:
            async with aiohttp.ClientSession() as session:
                async with session.post("https://hastebin.com/documents", data=message.clean_content) as r:
                    resp = await r.json()
                    try:
                        hb_url = "https://hastebin.com/{}".format(resp["key"])
                    except KeyError:
                        hb_url = "There was an error uploading to hb: {}".format(resp)
            if deleter:
                await self.ml_announce.send("in <#{}> a pretty big message by {} was deleted by {}, hastebin link: {}".format(message.channel.id, str(message.author), str(message.guild.get_member(deleter)), hb_url))
                return
            await self.ml_announce.send("{} in <#{}> deleted a pretty big message, hastebin link: {}".format(str(message.author), message.channel.id, hb_url))
            return
        if deleter:
            await self.ml_announce.send("in <#{}> a message by {} was deleted by {}:\n```{}```".format(message.channel.id, str(message.author), str(message.guild.get_member(deleter)), message.clean_content))
            return
        await self.ml_announce.send("{} in <#{}> deleted a message:\n```{}```".format(str(message.author), message.channel.id, message.clean_content))

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.channel_id != 588421329590419456:
            return
        # if payload.emoji.id == 358065563164999690:  # cadet
        #     await asyncio.sleep(1)
        #     await self.bot.get_guild(self.ml_guild).get_member(payload.user_id).add_roles(*[discord.Object(id=188030091148656641)])
        # if payload.emoji.id == 358066129345708032:  # eishi
        #     await asyncio.sleep(1)
        #     await self.bot.get_guild(self.ml_guild).get_member(payload.user_id).add_roles(*[discord.Object(id=173104384392167425)])
        # if payload.emoji.id == 358066125696794624:  # valk
        #     await asyncio.sleep(1)
        #     await self.bot.get_guild(self.ml_guild).get_member(payload.user_id).add_roles(*[discord.Object(id=173100534474080257)])
        # if payload.emoji.id == 593245318888292383:  # spoiler (check2)
        #     await asyncio.sleep(1)
        #     await self.bot.get_guild(self.ml_guild).get_member(payload.user_id).add_roles(*[discord.Object(id=180756419174203393)])
        # if payload.emoji.id == 593245068702253076:  # lewd (check1)
        #     await asyncio.sleep(1)
        #     await self.bot.get_guild(self.ml_guild).get_member(payload.user_id).add_roles(*[discord.Object(id=360896131015639042)])
        if payload.emoji.id == 593245363918602260:  # done (check3)
            await asyncio.sleep(1)
            await self.bot.get_guild(self.ml_guild).get_member(payload.user_id).remove_roles(*[discord.Object(id=588420756208353291)])
        await self.bot.get_guild(self.ml_guild).get_member(payload.user_id).add_roles(*self.ml_roles[payload.emoji.id])

def setup(bot):
    bot.add_cog(MuvLuv(bot))
