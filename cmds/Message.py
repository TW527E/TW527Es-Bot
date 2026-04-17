from datetime import datetime

import discord
from discord.ext import commands

from core.classes import Cog_Extension
from core.discord_helpers import avatar_url, delete_invocation
from core.loggee import Loggee


class Message(Cog_Extension):
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def say_msg(self, ctx, *, msg):
        await delete_invocation(ctx)
        Loggee(f"【指令】{ctx.author} 讓機器人複誦訊息")
        await ctx.send(msg)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def del_msg(self, ctx, num: int):
        await delete_invocation(ctx)
        deleted = await ctx.channel.purge(limit=max(0, min(num, 100)))
        Loggee(f"【指令】{ctx.author} 刪除 {len(deleted)} 則訊息")

    @commands.command(aliases=["dm"])
    @commands.has_permissions(administrator=True)
    async def say_dm(self, ctx, member: discord.Member, *, msg):
        await delete_invocation(ctx)
        await member.send(msg)

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        embed = discord.Embed(title="『私訊聊天室』", color=0xD08A2B)
        embed.set_thumbnail(url=avatar_url(member))
        embed.add_field(name="指定使用者", value=member.mention, inline=True)
        embed.add_field(name="指定的訊息", value=msg, inline=False)
        embed.set_footer(text=f"此指令由 {ctx.author} 輸入 • {now}", icon_url=avatar_url(ctx.author))
        await ctx.send(embed=embed)

    @commands.command()
    async def now_time(self, ctx):
        await delete_invocation(ctx)
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        await ctx.send(f"現在機器人的時間是 {now}")


async def setup(bot):
    await bot.add_cog(Message(bot))
