import discord
from discord.ext import commands


class Roles:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["roles"], pass_context=True, invoke_without_command=True)
    async def roleinfo(self, ctx):
        """Displays basic info about roles and channels

        Usage: `roles`
        If this outdated just mention it to Ako"""
        if "role_msg" not in self.bot.shit or self.bot.shit['role_msg'] is "":
            self.bot.shit['role_msg'] = "This is a (hopefully) current list of assignable roles and their meaning:\n" \
                                   "```Cadet: For those currently reading/planning to soon read Muv-Luv\n" \
                                   "Recruit: For those who have completed (or want to see spoilers for) Extra and Unlimited but not Alternative\n" \
                                   "Eishi: For those who have completed (or want to see spoilers for) Extra, Unlimited and Alternative\n" \
                                   "Valkyrie Member: For those who have completed (or want to see spoilers for) All Muv-Luv related content, including other VNs and shows\n" \
                                   "Spoiler Reader: Allows access to the message history of <#179284511803179008> and <#179284770210054145>. Be warned: These channels can have spoilers for anything at any time\n" \
                                   "theglob's works: This is a speacial rank that allows access to the channel moderator @theglob1981 uses for his endeavours in writing. of the focuses include his muv luv fanfiction, which has trilogy spoilers```\n" \
                                   "These roles dictate which spoiler channels you can view, and can be added using the `roles add [name]` command"
        await self.bot.say(self.bot.shit['role_msg'], delete_after=60)  # Time can be adjusted/changed to a PM if the need arises

    @commands.command(aliases=["add role", ], pass_context=True, no_pm=True)
    async def roleadd(self, ctx, *, role: str):
        """Add a role from the list mentioned in the `roles` command

        Currently accepted role names (case-insensitive):
        Cadet, Recruit, Eishi, Valkyrie, Valkyrie Member, Spoiler, Spoiler Reader, Muv Luv Alternative Divergence, Divergence, Alternative Divergence, Fanfic, MLAD
        Please note roles currently cannot be removed via the bot, so choose wisely, and mute potential spoiler channels you don't wish to read"""
        cadet = discord.utils.get(ctx.message.server.roles, id="188030091148656641")
        recruit = discord.utils.get(ctx.message.server.roles, id="173104384392167425")
        eishi = discord.utils.get(ctx.message.server.roles, id="173100677793316865")
        valkyrie = discord.utils.get(ctx.message.server.roles, id="173100534474080257")
        spoiler = discord.utils.get(ctx.message.server.roles, id="180756419174203393")
        mlad = discord.utils.get(ctx.message.server.roles, id="185872382886412297")  # was Muv Luv Alternative Divergence, now theglob's works
        role = role.split()  # I'm a dum and thought it was already a list, whoops

        if len(ctx.message.mentions) != 0 and any([r.permissions.manage_messages for r in ctx.message.author.roles]):  # Roll adding for mods, useful for mobile
            if role[0].lower() == "cadet":
                await self.bot.say("👌")
                for m in ctx.message.mentions:
                    await self.bot.add_roles(m, cadet)
                return
            if role[0].lower() == "recruit":
                await self.bot.say("👌")
                for m in ctx.message.mentions:
                    await self.bot.add_roles(m, cadet, recruit)
                return
            if role[0].lower() == "eishi":
                await self.bot.say("👌")
                for m in ctx.message.mentions:
                    await self.bot.add_roles(m, cadet, recruit, eishi)
                return
            if role[0].lower() == "valkyrie":
                await self.bot.say("👌")
                for m in ctx.message.mentions:
                    await self.bot.add_roles(m, cadet, recruit, eishi, valkyrie)
                return
            if role[0].lower() == "spoiler":
                await self.bot.say("👌")
                for m in ctx.message.mentions:
                    await self.bot.add_roles(m, spoiler)
                return
            if role[0].lower() == "glob" or role[0].lower() == "glob's" or role[0].lower() == "theglob" or role[0].lower() == "theglob's":
                await self.bot.say("👌")
                for m in ctx.message.mentions:
                    await self.bot.add_roles(m, mlad)
                return
            await self.bot.say("Please choose a valid role!")

        else:
            if role[0].lower() == "cadet":
                await self.bot.say(ctx.message.author.mention + " 👌")
                await self.bot.add_roles(ctx.message.author, cadet)
                return
            if role[0].lower() == "recruit":
                await self.bot.say(ctx.message.author.mention + " 👌")
                await self.bot.add_roles(ctx.message.author, cadet, recruit)
                return
            if role[0].lower() == "eishi":
                await self.bot.say(ctx.message.author.mention + " 👌")
                await self.bot.add_roles(ctx.message.author, cadet, recruit, eishi)
                return
            if role[0].lower() == "valkyrie":
                await self.bot.say("👌")
                await self.bot.add_roles(ctx.message.author, cadet, recruit, eishi, valkyrie)
                return
            if role[0].lower() == "spoiler":
                await self.bot.say("👌")
                await self.bot.add_roles(ctx.message.author, spoiler)
                return
            if role[0].lower() == "glob" or role[0].lower() == "glob's" or role[0].lower() == "theglob" or role[0].lower() == "theglob's":
                await self.bot.say("👌")
                await self.bot.add_roles(ctx.message.author, mlad)
                return
            await self.bot.say("Please choose a valid role!")


def setup(bot):
    bot.add_cog(Roles(bot))
