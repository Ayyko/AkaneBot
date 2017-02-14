import discord
from discord.ext.commands import check

owner_id = "132694825454665728"


def is_owner():
    return check(lambda ctx: ctx.message.author.id == owner_id)


def has_perm(perm):
    def inner(ctx):
        return getattr(ctx.message.author.server_permissions, perm)
    return check(inner)
