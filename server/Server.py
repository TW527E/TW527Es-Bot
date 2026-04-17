import discord
from discord.ext import commands

from core.classes import Cog_Extension
from core.discord_helpers import avatar_url, delete_invocation, guild_icon_url
from core.loggee import Loggee


class Server(Cog_Extension):
    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def set_server_name(self, ctx, *, name):
        await delete_invocation(ctx)
        before = ctx.guild.name
        await ctx.guild.edit(name=name, reason=f"{ctx.author} changed server name")

        icon = guild_icon_url(ctx.guild)
        embed = discord.Embed(title="『指令-更改伺服器名稱』", color=0xD08A2B)
        if icon:
            embed.description = f"[點此到達伺服器頭像連結]({icon})"
            embed.set_thumbnail(url=icon)
        embed.add_field(name="更改前的伺服器名稱", value=before, inline=True)
        embed.add_field(name="更改後的伺服器名稱", value=name, inline=False)
        embed.set_footer(text=f"此指令由 {ctx.author} 輸入", icon_url=avatar_url(ctx.author))
        Loggee(f"『指令-更改伺服器名稱』 {ctx.author.name} 在 {before} 修改伺服器名稱為 {name}")
        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    async def add_role(self, ctx, member: discord.Member, *, role: discord.Role):
        await delete_invocation(ctx)
        await member.add_roles(role, reason=f"{ctx.author} used add_role")
        await self._send_role_embed(ctx, "增加使用者身分組", member, role)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    async def remove_role(self, ctx, member: discord.Member, *, role: discord.Role):
        await delete_invocation(ctx)
        await member.remove_roles(role, reason=f"{ctx.author} used remove_role")
        await self._send_role_embed(ctx, "刪除使用者身分組", member, role)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    async def create_role(self, ctx, *, name):
        await delete_invocation(ctx)
        role = await ctx.guild.create_role(name=name, reason=f"{ctx.author} created role")
        await ctx.send(f"已建立身分組 {role.mention}")

    @commands.command()
    @commands.guild_only()
    async def roles(self, ctx):
        roles = [role.mention for role in ctx.guild.roles if role.name != "@everyone"]
        embed = discord.Embed(title="『群內所有身分組』", description="群內所有身分組", color=0xD08A2B)
        icon = guild_icon_url(ctx.guild)
        if icon:
            embed.set_thumbnail(url=icon)
        embed.add_field(name="群組", value=ctx.guild.name, inline=True)
        embed.add_field(name="身分組", value=", ".join(roles) or "無", inline=False)
        embed.set_footer(text=f"此指令由 {ctx.author} 輸入", icon_url=avatar_url(ctx.author))
        await ctx.send(embed=embed)

    async def _send_role_embed(self, ctx, title, member, role):
        embed = discord.Embed(title=f"『{title}』", color=0xD08A2B)
        embed.set_thumbnail(url=avatar_url(member))
        embed.add_field(name="使用者", value=member.mention, inline=True)
        embed.add_field(name="身分組", value=role.mention, inline=False)
        embed.set_footer(text=f"此指令由 {ctx.author} 輸入", icon_url=avatar_url(ctx.author))
        Loggee(f"『{title}』 {ctx.author.name} 在 {ctx.guild.name} 對 {member} 操作 {role}")
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Server(bot))
