import aiohttp
import discord
from .utils import checks


class NSA:
    def __init__(self, bot):
        self.bot = bot
        self.log_chan = self.bot.get_channel(291681699043999754)
        self.log_list = [203903748597219328, 227166775626825729, 133665049406472192, 132988506778632193, 205762560912261120, 273014576394665985]

    async def on_message_delete(self, message):
        if not message.content:
            print("no content")
            return
        if message.channel.id not in self.log_list:
            return
        if len(message.clean_content) > 1900:
            async with aiohttp.ClientSession() as session:
                async with session.post("https://hastebin.com/documents", data=message.clean_content) as r:
                    resp = await r.json()
                    try:
                        hb_url = "https://hastebin.com/{}".format(resp["key"])
                    except KeyError:
                        hb_url = "There was an error uploading to hb: {}".format(resp)
            await self.log_chan.send("{} in #{} ({}) deleted {}".format(str(message.author),message.channel.name, message.guild.name, hb_url))
            print("long del")
            return
        await self.log_chan.send("{} in #{} ({}) deleted:\n```{}```".format(str(message.author), message.channel.name, message.guild.name, message.clean_content))
        print("shor del")

    async def on_message_edit(self, before, after):
        if not after.content:
            return
        if after.channel.id not in self.log_list:
            return
        ret = "before:\n{}\nafter:\n{}".format(before.clean_content, after.clean_content)
        if len(ret) > 1900:
            async with aiohttp.ClientSession() as session:
                async with session.post("https://hastebin.com/documents", data=ret) as r:
                    resp = await r.json()
                    try:
                        hb_url = "https://hastebin.com/{}".format(resp["key"])
                    except KeyError:
                        hb_url = "There was an error uploading to hb: {}".format(resp)
            await self.log_chan.send("{} in #{} ({}) edited {}".format(str(after.author), after.channel.name, after.guild.name, hb_url))
            return
        await self.log_chan.send("{} in #{} ({}) edited:\n```{}```".format(str(after.author), after.channel.name, after.guild.name, ret))


def setup(bot):
    bot.add_cog(NSA(bot))
