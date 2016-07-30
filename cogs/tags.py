import discord
from discord.ext import commands


class Tags:
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="tags", pass_context=True, no_pm=True, enabled=False)
    async def tag(self, ctx):
        """Lists all tags that can be used in the current channel

            Usage: `tags`
            New tags can be added with the `tag add` command.
            A list of all tags can be received in pm by using the `tag all` command. (watch out for possible spoilers in the tag names)
            A list of a specific channel's tag list can be received in pm by using the 'tag channel [#channel_name]' command"""
        ret = ""
        if ctx.message.channel.id in self.bot.shit['tags'] and self.bot.shit['tags'][ctx.message.channel.id]:
            ret += "Channel specific tags:\n" + ", ".join(self.bot.shit['tags'][ctx.message.channel.id]) + "\n"
        ret += "Global tags:\n" + ", ".join(self.bot.shit['tags']["global"])
        await self.bot.say(ret)

    @tag.command(pass_context=True, no_pm=True)
    async def create(self, ctx, name, *, tag_content):
        """Create a new channel specific tag.

        Usage: `tag create [name] [content]`
        By default the new tag is only accessible in the channel it was made.
        To create a tag for use in any channel, use the `tag server` command
        """
        if name in self.bot.commands:
            await self.bot.say("Sorry, {} is the name of one of the bots commands, choose another".format(name))
            return

        if name in self.bot.shit['tags'][ctx.message.channel.id]:
            await self.bot.say("A tag with this name already exists in this channel")
            return

        if name in self.bot.shit['tags']['global']:
            await self.bot.say("A server tag with that name already exists")
            return

        self.bot.shit['tags'][ctx.message.channel.id][name] = {"content": tag_content, "owner": ctx.message.author.id}
        await self.bot.say("Tag {} created successfully for use in this channel".format(name))

    @tag.command(pass_context=True)
    async def server(self, ctx, name, *, tag_content):
        """Create a new server tag, usable in any channel.

        Usage: `tag server [name] [content]`
        For any possible spoiler, please use the `tag create` command instead, to prevent spoilers from leaving their relevant channels.
        Misuse of server tags will be severely punished, constant misuse may result in it being only usable by certain members"""
        if name in self.bot.commands:
            await self.bot.say("Sorry, {} is the name of one of the bots commands, choose another".format(name))
            return

        if name in self.bot.shit['tags']['global']:
            await self.bot.say("A server tag with that name already exists")
            return

        for chan in self.bot.shit['tags']:
            if name in self.bot.shit['tags'][chan]:
                await self.bot.say("A tag with this name has already been made for the {}.name channel".format(self.bot.get_channel(chan)))
                return

        self.bot.shit['tags']['global'][name] = {"content": tag_content, "owner": ctx.message.author.id}
        await self.bot.say("Sever tag {} created successfully".format(name))
        save()

    @tag.command(pass_context=True, no_pm=True)
    async def remove(self, ctx, name):
        """Remove a tag by name.

        Usage `tag remove [name]`
        Attempts to remove Channel specific tag from the channel of the message before moving on to checking server-wide tags
        Tag owners and Mods are the only ones allowed to remove tags"""
        if any([n == name for n in self.bot.shit['tags'][ctx.message.channel.id]]):
            if any([r.permissions.manage_messages for r in ctx.message.author.roles]) or self.bot.shit['tags'][ctx.message.channel.id][name]['owner'] == ctx.message.author.id:
                del self.bot.shit['tags'][ctx.message.channel.id][name]
                await self.bot.say("Channel specific tag {} has been removed".format(name))
                return
            await self.bot.say("Only the owner or a mod can remove tags")

        elif any([n == name for n in self.bot.shit['tags']['global']]):
            if any([r.permissions.manage_messages for r in ctx.message.author.roles]) or self.bot.shit['tags']['global'][name]['owner'] == ctx.message.author.id:
                del self.bot.shit['tags']['global'][name]
                await self.bot.say("Server tag {} has been removed".format(name))
                return
            await self.bot.say("Only the owner or a mod can remove tags")

        else:
            await self.bot.say("No tag with that name exists")


def setup(bot):
    bot.add_cog(Tags(bot))
