import discord
from discord.ext import commands
import urllib
import aiohttp
import re


class Animanga(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener(name="on_message")
    async def anime_search(self, message):
        regex = r"{{(.+?)}}"
        if not message.guild:
            return
        if message.guild.id in self.bot.shit['anime_guilds']:
            matches = re.findall(regex, message.content)
            for match in matches:
                if match.lower() in self.bot.shit["anime_syns"]:
                    title = urllib.parse.quote(self.bot.shit["anime_syns"][match.lower()])
                else:
                    title = urllib.parse.quote(match)
                base_url = "https://api.jikan.moe/v3/search/anime?q="
                try:
                    async with aiohttp.ClientSession() as session:
                        async with session.get(base_url+title) as resp:
                            if resp.status == 200:
                                results = await resp.json()
                            else:
                                await message.channel.send("Something went wrong.")
                                print(resp)
                                return
                    if "results" in results and results["results"]:
                        await message.channel.send("<" + results["results"][0]["url"] + ">")
                    else:
                        await message.channel.send("Anime not found.")
                except Exception as e:
                    await message.channel.send("Something went wrong. Error: " + str(e))

    @commands.Cog.listener(name="on_message")
    async def manga_search(self, message):
        regex = r"\[\[(.+?)\]\]"
        if not message.guild:
            return
        if message.guild.id in self.bot.shit['anime_guilds']:
            matches = re.findall(regex, message.content)
            for match in matches:
                if match.lower() in self.bot.shit["manga_syns"]:
                    title = urllib.parse.quote(self.bot.shit["manga_syns"][match.lower()])
                else:
                    title = urllib.parse.quote(match)
                base_url = "https://api.jikan.moe/v3/search/manga?q="
                try:
                    async with aiohttp.ClientSession() as session:
                        async with session.get(base_url + title) as resp:
                            if resp.status == 200:
                                results = await resp.json()
                            else:
                                await message.channel.send("Something went wrong.")
                                print(resp)
                                return
                    if "results" in results and results["results"]:
                        await message.channel.send("<" + results["results"][0]["url"] + ">")
                    else:
                        await message.channel.send("Manga not found.")
                except Exception as e:
                    await message.channel.send("Something went wrong. Error: " + str(e))

    @commands.command(name="add syn", aliases=["add synonym", "add anime", "aadd", "addanime"])
    async def add_syn(self, ctx, syn, *, anime):
        self.bot.shit["anime_syns"][syn.lower()] = anime
        await ctx.send("Synonym added")

    @commands.command(name="add manga", aliases=["addmanga"])
    async def add_manga(self, ctx, syn, *, manga):
        self.bot.shit["manga_syns"][syn.lower()] = manga
        await ctx.send("Synonym added")


def setup(bot):
    bot.add_cog(Animanga(bot))
