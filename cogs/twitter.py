import random
import aiohttp
import discord
from discord.ext import commands


class Twitter:
    def __init__(self, bot):
        self.bot = bot
        self.base_url = "https://api.twitter.com/1.1/"
        self.timeline_endpoint = "statuses/user_timeline.json"
        self.timeline_url = self.base_url + self.timeline_endpoint
        self.user_agent = "Akane Discord Bot v2.0.0"
        self.token = "Bearer " + self.bot.shit["twitter"]

    @commands.command(name="get tweets", aliases=["tget", "get tweet"])
    async def gettweets(self, ctx, user, number=1):
        """Returns the last number tweets from user, max 3"""
        number = number if number < 3 else 3
        tweets = await self.get_tweets(user)
        for t in range(number):
            tweet = tweets[t]
            title = tweet["user"]["name"]
            url = "https://twitter.com/statuses/" + str(tweet["id"])
            description = tweet["text"]
            embed = discord.Embed(title=title, url=url, description=description)
            try:
                embed.set_image(url=tweet["entities"]["media"][0]["media_url"])
            except KeyError:
                pass
            embed.set_footer(text="Powered by Twitter", icon_url="https://cdn.cms-twdigitalassets.com/content/brand-twitter/en/jcr:content/par/c01_column_1596992668/col2/b04_asset_download_m.img.500.medium.1469476604231.jpg")

            await ctx.send(embed=embed)

    @commands.command(name="random tweets", aliases=["rtweet", "trand", "random tweet"])
    async def randtweet(self, ctx, user, number=1):
        """Returns number random tweets from user, max 3"""
        number = number if number < 3 else 3
        tweets = await self.get_tweets(user)
        for t in range(number):
            tweet = random.choice(tweets)
            tweets.remove(tweet)
            title = tweet["user"]["name"]
            url = "https://twitter.com/statuses/" + str(tweet["id"])
            description = tweet["text"]
            embed = discord.Embed(title=title, url=url, description=description)
            try:
                embed.set_image(url=tweet["entities"]["media"][0]["media_url"])
            except KeyError:
                pass
            embed.set_footer(text="Powered by Twitter", icon_url="https://cdn.cms-twdigitalassets.com/content/brand-twitter/en/jcr:content/par/c01_column_1596992668/col2/b04_asset_download_m.img.500.medium.1469476604231.jpg")

            await ctx.send(embed=embed)

    async def get_tweets(self, user, **options):
        params = {"screen_name": user, "count": 200, "include_rts": "false"}
        params.update(options)
        headers = {"User-Agent": self.user_agent, "Authorization": self.token}
        async with aiohttp.ClientSession() as client:
            async with client.get(self.timeline_url, headers=headers, params=params) as resp:
                if resp.status == 404:
                    raise commands.BadArgument
                if resp.status != 200:
                    raise commands.CommandError("Failed to get tweets")
                return await resp.json()


def setup(bot):
    bot.add_cog(Twitter(bot))
