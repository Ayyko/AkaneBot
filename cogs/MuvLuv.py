import discord
from discord.ext import commands
import aiohttp

class MuvLuv:
    def __init__(self, bot):
        self.bot = bot
        self.ml_server = "169056767219597312"
        self.ml_announce = self.bot.get_channel("235502028930023424")

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
                async with session.post("hastebin.com/documents", ret) as r:
                    resp = await r.json()
                    hb_url = "http://hastebin.com/{}".format(resp["key"])
            await self.bot.send_message(self.ml_announce, "{} in #{} edited a pretty big message, hastebin link: {}".format(after.author.mention, after.channel.name, hb_url))
            return
        await self.bot.send_message(self.ml_announce, "{} in #{} edited a message:\n ```diff\n{}```".format(after.author.mention, after.channel.name, ret))

    async def on_message_delete(self, message):
        if message.server != self.ml_server:
            return
        if message.channel == self.ml_announce:
            return
        if len(message.clean_content) > 1900:
            async with aiohttp.ClientSession() as session:
                async with session.post() as r:
                    resp = await r.json()
                    hb_url = "http://hastebin.com/{}".format(resp["key"])
            await self.bot.send_message(self.ml_announce, "{} in #{} deleted a pretty big message, hastebin link: {}".format(message.author.mention, message.channel.name, hb_url))
            return
        await self.bot.send_message(self.ml_announce, "{} in #{} deleted a message:\n```{}```".format(message.author.mention, message.channel.name, message.clean_content))

# HASTEBIN NOTES :  post to hastebin.com/documents     you get a response {'key': 'ukemuguzaf'}

def setup(bot):
    bot.add_cog(MuvLuv(bot))
