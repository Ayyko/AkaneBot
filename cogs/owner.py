import discord
from discord.ext import commands
from cogs.utils import checks
import inspect

class Owner:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="eval", pass_context=True, hidden=True)
    @checks.is_owner()
    async def _eval(self, ctx, *, code: str):
        """Extremely unsafe eval command."""
        code = code.strip('` ')
        python = '```py\n{}\n```'
        result = None

        env = {
            'bot': self.bot,
            'ctx': ctx,
            'message': ctx.message,
            'server': ctx.message.server,
            'channel': ctx.message.channel,
            'author': ctx.message.author
        }

        env.update(globals())

        try:
            result = eval(code, env)
            if inspect.isawaitable(result):
                result = await result
        except Exception as e:
            await self.bot.say(python.format(type(e).__name__ + ': ' + str(e)))
            return

        await self.bot.say(python.format(result))

    @commands.command(pass_context=True, hidden=True)
    @checks.is_owner()
    async def die(self, ctx, hidden=True):
        await self.bot.say("Bye-bye")
        await self.bot.logout()



def setup(bot):
    bot.add_cog(Owner(bot))