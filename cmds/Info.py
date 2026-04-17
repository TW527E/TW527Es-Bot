import discord
from discord.ext import commands

from core.classes import Cog_Extension
from core.discord_helpers import avatar_url, delete_invocation, guild_icon_url


STATUS_TEXT = {
    "online": "線上",
    "offline": "離線",
    "idle": "閒置",
    "dnd": "請勿打擾",
}


class Info(Cog_Extension):
    @commands.command()
    @commands.guild_only()
    async def guild(self, ctx):
        await delete_invocation(ctx)
        guild = ctx.guild
        icon = guild_icon_url(guild)
        embed = discord.Embed(title=guild.name, color=0xD08A2B)
        if icon:
            embed.description = f"[點此到達伺服器頭像連結]({icon})"
            embed.set_thumbnail(url=icon)
        embed.add_field(name="伺服器名稱", value=guild.name, inline=True)
        embed.add_field(name="伺服器擁有者", value=str(guild.owner), inline=False)
        embed.add_field(name="偏好語言", value=str(guild.preferred_locale), inline=True)
        embed.add_field(name="伺服器創建日期", value=guild.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=False)
        embed.add_field(name="伺服器 ID", value=str(guild.id), inline=True)
        embed.add_field(name="伺服器目前成員數量", value=str(guild.member_count), inline=False)
        embed.set_footer(text=f"此指令由 {ctx.author} 輸入", icon_url=avatar_url(ctx.author))
        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def info(self, ctx, member: discord.Member = None):
        await delete_invocation(ctx)
        member = member or ctx.author
        url = avatar_url(member)
        roles = [role.mention for role in member.roles if role.name != "@everyone"]
        status = STATUS_TEXT.get(str(member.status), "無法得知")
        activity = str(member.activity) if member.activity else "沒有"

        embed = discord.Embed(title=str(member), description=f"[點此到達頭像連結]({url})", color=0xD08A2B)
        embed.set_thumbnail(url=url)
        embed.add_field(name="使用者名稱", value=member.name, inline=True)
        embed.add_field(name="目前狀態", value=status, inline=False)
        embed.add_field(name="目前狀態消息", value=activity, inline=True)
        embed.add_field(name="此帳號創建日期", value=member.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=False)
        embed.add_field(
            name="此帳號加入此群日期",
            value=member.joined_at.strftime("%Y-%m-%d %H:%M:%S") if member.joined_at else "未知",
            inline=True,
        )
        embed.add_field(name="在此群擁有的所有身分組", value=", ".join(roles) or "無", inline=False)
        embed.add_field(name="使用者是否為機器人", value="是機器人" if member.bot else "不是機器人", inline=True)
        embed.add_field(name="使用者 ID", value=str(member.id), inline=False)
        embed.set_footer(text=f"此指令由 {ctx.author} 輸入", icon_url=avatar_url(ctx.author))
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Info(bot))
