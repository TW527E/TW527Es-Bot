import discord
from discord.ext import commands

from core.classes import Cog_Extension
from core.config import get_owner_id, get_settings
from core.discord_helpers import avatar_url, delete_invocation
from core.loggee import Loggee


BOT_DISPLAY_NAME = "TW527E的機器人"


class Main(Cog_Extension):
    @commands.command()
    async def ping(self, ctx):
        await delete_invocation(ctx)
        embed = discord.Embed(title=BOT_DISPLAY_NAME, description="Ping值", color=0x28D252)
        embed.add_field(name="目前 Ping 值", value=f"{round(self.bot.latency * 1000)} 毫秒(ms)", inline=True)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await delete_invocation(ctx)
        await member.kick(reason=reason)
        Loggee(f"《指令》〔{ctx.author}〕 踢出 {member}，原因: {reason or '未提供'}")
        await ctx.send(f"使用者 **{member}** 已被踢出")

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await delete_invocation(ctx)
        await member.ban(reason=reason)
        Loggee(f"《指令》〔{ctx.author}〕 封鎖 {member}，原因: {reason or '未提供'}")
        await ctx.send(f"使用者 **{member}** 已被封鎖")

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        await delete_invocation(ctx)
        member_name, _, member_discriminator = member.partition("#")

        async for ban_entry in ctx.guild.bans(limit=None):
            user = ban_entry.user
            if user.name == member_name and user.discriminator == member_discriminator:
                await ctx.guild.unban(user)
                Loggee(f"《指令》〔{ctx.author}〕 解除封鎖 {user}")
                await ctx.send(f"使用者 **{user}** 已經解除封鎖")
                return

        await ctx.send("找不到這位被封鎖的使用者。")

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_nicknames=True)
    async def rename(self, ctx, member: discord.Member, *, name):
        await delete_invocation(ctx)

        settings = get_settings()
        owner_id = get_owner_id(settings)
        if self.bot.user and member.id == self.bot.user.id and ctx.author.id != owner_id:
            await ctx.send(f"『想幹嘛阿』**{ctx.author.mention}** 想幹嘛阿!")
            return

        before = member.display_name
        await member.edit(nick=name)
        await ctx.send(f"『更改名稱』**{before}** 的暱稱已被變更為: **{name}**")

    @commands.command()
    @commands.guild_only()
    async def nick(self, ctx, *, name):
        await delete_invocation(ctx)
        before = ctx.author.display_name
        await ctx.author.edit(nick=name)

        embed = discord.Embed(title=f"『更改 {ctx.author.name} 名稱』", color=0xD08A2B)
        embed.set_thumbnail(url=avatar_url(ctx.author))
        embed.add_field(name="更改前的名稱", value=before, inline=True)
        embed.add_field(name="更改後的名稱", value=name, inline=False)
        embed.set_footer(text=f"此指令由 {ctx.author} 輸入", icon_url=avatar_url(ctx.author))
        await ctx.send(embed=embed)

    @commands.command()
    async def avatar(self, ctx, member: discord.Member = None):
        await delete_invocation(ctx)
        member = member or ctx.author
        url = avatar_url(member)

        embed = discord.Embed(title=str(member), description=f"[點此到達頭像連結]({url})", color=0xD08A2B)
        embed.set_image(url=url)
        embed.set_footer(text=f"此指令由 {ctx.author} 輸入", icon_url=avatar_url(ctx.author))
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Main(bot))
