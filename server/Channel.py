from discord.ext import commands

from core.classes import Cog_Extension
from core.discord_helpers import delete_invocation


class Channel(Cog_Extension):
    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    async def add_text_ch(self, ctx, *, name):
        await delete_invocation(ctx)
        channel = await ctx.guild.create_text_channel(name, reason=f"{ctx.author} created by command")
        await ctx.send(f"《文字頻道》已建立 {channel.mention}")

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    async def add_voice_ch(self, ctx, *, name):
        await delete_invocation(ctx)
        channel = await ctx.guild.create_voice_channel(name, reason=f"{ctx.author} created by command")
        await ctx.send(f"《語音頻道》已建立 **{channel.name}**")


async def setup(bot):
    await bot.add_cog(Channel(bot))
