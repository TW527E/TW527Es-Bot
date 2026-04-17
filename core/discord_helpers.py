from contextlib import suppress

import discord


def avatar_url(user):
    return str(user.display_avatar.url)


def guild_icon_url(guild):
    if guild.icon is None:
        return ""
    return str(guild.icon.url)


async def delete_invocation(ctx):
    with suppress(discord.Forbidden, discord.NotFound):
        await ctx.message.delete()


async def send_temporary(ctx, content, seconds=5):
    await ctx.send(content, delete_after=seconds)
