import discord
from discord import app_commands
from discord.ext import commands

from core.classes import Cog_Extension
from core.discord_helpers import avatar_url, guild_icon_url
from core.interactions import chunk_values, respond


STATUS_TEXT = {
    "online": "線上",
    "offline": "離線",
    "idle": "閒置",
    "dnd": "請勿打擾",
}


class Info(Cog_Extension):
    @app_commands.command(name="guild", description="查看伺服器資訊")
    @app_commands.guild_only()
    async def guild(self, interaction: discord.Interaction):
        guild = interaction.guild
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
        embed.set_footer(text=f"此指令由 {interaction.user} 輸入", icon_url=avatar_url(interaction.user))
        await respond(interaction, embed=embed, ephemeral=True)

    @app_commands.command(name="info", description="查看使用者資訊")
    @app_commands.describe(member="要查看的成員，留空則查看自己")
    @app_commands.guild_only()
    async def info(self, interaction: discord.Interaction, member: discord.Member | None = None):
        member = member or interaction.user
        url = avatar_url(member)
        roles = [role.mention for role in member.roles if role.name != "@everyone"]
        status = STATUS_TEXT.get(str(member.status), "無法得知")
        activity = str(member.activity) if member.activity else "沒有"

        embed = discord.Embed(title=str(member), description=f"[點此到達頭像連結]({url})", color=0xD08A2B)
        embed.set_thumbnail(url=url)
        embed.add_field(name="使用者名稱", value=member.name, inline=True)
        embed.add_field(name="目前狀態", value=status, inline=False)
        embed.add_field(name="目前狀態消息", value=activity[:1024], inline=True)
        embed.add_field(name="此帳號創建日期", value=member.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=False)
        embed.add_field(
            name="此帳號加入此群日期",
            value=member.joined_at.strftime("%Y-%m-%d %H:%M:%S") if member.joined_at else "未知",
            inline=True,
        )
        for index, chunk in enumerate(chunk_values(roles), start=1):
            name = "在此群擁有的所有身分組" if index == 1 else f"身分組 {index}"
            embed.add_field(name=name, value=chunk, inline=False)
        embed.add_field(name="使用者是否為機器人", value="是機器人" if member.bot else "不是機器人", inline=True)
        embed.add_field(name="使用者 ID", value=str(member.id), inline=False)
        embed.set_footer(text=f"此指令由 {interaction.user} 輸入", icon_url=avatar_url(interaction.user))
        await respond(interaction, embed=embed, ephemeral=True)


async def setup(bot):
    await bot.add_cog(Info(bot))
