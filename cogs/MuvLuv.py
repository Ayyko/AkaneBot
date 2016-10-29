import discord
from discord.ext import commands

class MuvLuv:
    def __init__(self, bot):
        self.bot = bot
        self.ml_server = "169056767219597312"
        self.ml_announce = "235502028930023424"

    async def on_member_join(self, member):
        announce = await self.bot.get_channel(self.ml_announce)
        if member.server.id == self.ml_server:
            await self.bot.send_message(announce, "@here Member joined: {a.name}, {a.mention}".format(a=member))

    async def on_member_remove(self, member):
        announce = await self.bot.get_channel(self.ml_announce)
        if member.server.id == self.ml_server:
            await self.bot.send_message(announce, "Member left: {a.name}, ({a.id})".format(a=member))

    async def on_member_ban(self, member):
        announce = await self.bot.get_channel(self.ml_announce)
        if member.server.id == self.ml_server:
            await self.bot.send_message(announce, "🔨🔨 Member banned: {a.name}, ({a.id})".format(a=member))

    async def on_member_unban(self, member):
        announce = await self.bot.get_channel(self.ml_announce)
        if member.server.id == self.ml_server:
            await self.bot.send_message(announce, "Member unbanned: {a.name}, ({a.id})".format(a=member))


def setup(bot):
    bot.add_cog(MuvLuv(bot))
