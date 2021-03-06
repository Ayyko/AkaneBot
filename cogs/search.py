from discord.ext import commands
from cogs.utils import checks
import aiohttp
import urllib


class Search(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.base_url = "https://www.googleapis.com/customsearch/v1"
        self.params = {'cx': self.bot.shit['google']['cx'], 'key': self.bot.shit['google']['key'], 'q': ''}
        self.nsfw = False  # Doesn't do anything yet

    @commands.command(aliases=["listsearch", "list search"])
    async def lsearch(self, ctx, *, query):
        """Google search that returns a list of links to results.

        Defaults to five results
        Usage: {prefix}lsearch [results] <query>"""
        num = 5
        num_error = 0

        if query.split()[0].isdigit():
            num = int(query.split()[0])
            if num > 10:
                num_error = 1
                num = 10
            query = "+".join(query.split()[1:])
        self.params['q'] = urllib.parse.quote_plus(query, encoding='utf-8', errors='replace')
        async with aiohttp.ClientSession() as session:
            async with session.get(self.base_url + "?key={}&cx={}&q={}&safe=high".format(self.params['key'], self.params['cx'], self.params['q'])) as r:  # built in aiohtttp params thing didn't work so we got this cancer
                results = await r.json()  # TODO: make safe search toggleable/have a flag for it/smth
        try:
            if results["searchInformation"]["totalResults"] is not "0":
                if int(results["searchInformation"]["totalResults"]) < num:
                    num = int(results["searchInformation"]["totalResults"])
                    num_error = 2
                ret = ""
                for i in range(num):
                    emoji = await self.emoji_get(i)
                    ret += "{} `{}` <{}>\n".format(emoji, results["items"][i]["title"], results["items"][i]["link"])
                if num_error == 1:
                    ret += "Results have been limited to 10 because that's how many google returns"
                elif num_error == 2:
                    ret += "Results have been limited to {}".format(num)
                ret = "Results for `" + query.replace("@here", "@​here").replace("@everyone", "@​everyone") + "`\n" + ret.replace("@here", "@​here").replace("@everyone", "@​everyone")
                await ctx.send(ret[:1999])
            else:
                await ctx.send("No results found for {}".format(query.replace("@here", "@​here").replace("@everyone", "@​everyone")))
            # print(json.dumps(results))
        except KeyError:
            try:
                results["error"]["errors"]
                await ctx.send("API returned error(s):")
                for error in results["error"]["errors"]:
                    await ctx.send("`" + error["domain"] + ": " + error["reason"] + "`")
                    print(error)
            except KeyError as e:
                await ctx.send("An unknown error has occurred, tell Ako you broke it")
                print(e)

    @commands.command(pass_context=True)
    async def search(self, ctx, *, query):
        """Google search

        Defaults to one result
        Usage: {prefix}search [results] <query>"""
        num = 1
        num_error = 0
        if query.split()[0].isdigit():
            num = int(query.split()[0])
            if num < 1:
                query += "+{}".format(num)
            if num > 10:
                num_error = 2
                num = 10
            if num > 5 and not ctx.message.author.id == checks.owner_id:
                num_error = 1
                num = 5  # TODO:
            query = "+".join(query.split()[1:])
        self.params['q'] = urllib.parse.quote_plus(query, encoding='utf-8', errors='replace')
        async with aiohttp.ClientSession() as session:
            async with session.get(self.base_url + "?key={}&cx={}&q={}&safe=high".format(self.params['key'], self.params['cx'], self.params['q'])) as r:  # built in aiohtttp params thing didn't work so we got this cancer
                results = await r.json()

        try:
            if results["searchInformation"]["totalResults"] is not "0":
                if int(results["searchInformation"]["totalResults"]) < num:
                    num = int(results["searchInformation"]["totalResults"])
                    num_error = 1
                ret = ""
                for i in range(num):
                    emoji = await self.emoji_get(i)
                    ret += "{} `{}`\n{}\n{}\n\n".format(emoji, results["items"][i]["title"], results["items"][i]["link"], results["items"][i]["snippet"])
                if num_error == 1:
                    ret += "Results have been limited to {}".format(num)
                if num_error == 2:
                    ret += "Results have been limited to 10 because google only gives me 10 at a time"
                ret = "Results for `" + query.replace("@here", "@​here").replace("@everyone", "@​everyone") + "`\n" + ret.replace("@here", "@​here").replace("@everyone", "@​everyone")
                await ctx.send(ret[:1999])
            else:
                await ctx.send("No results found for {}".format(query.replace("@here", "@​here").replace("@everyone", "@​everyone")))

        except KeyError:
            try:
                results["error"]["errors"]
                await ctx.send("API returned error(s):")
                for error in results["error"]["errors"]:
                    await ctx.send("`" + error["domain"] + ": " + error["reason"] + "`")
                    print(error)
            except KeyError as e:
                await ctx.send("An unknown error has occurred, tell Ako you broke it")
                print(e)

    async def emoji_get(self, i):
        emoji_list = [':one:', ':two:', ':three:', ':four:', ':five:', ':six:', ':seven:', ':eight:', ':nine:', ':keycap_ten:']
        if i < 10:
            return emoji_list[i]
        return "  "


def setup(bot):
    bot.add_cog(Search(bot))
