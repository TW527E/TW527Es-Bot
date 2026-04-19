import discord
from discord import app_commands
from discord.ext import commands

from core.classes import Cog_Extension
from core.config import int_or_none
from core.discord_helpers import avatar_url
from core.interactions import respond
from core.loggee import Loggee


BOT_DISPLAY_NAME = "TW527E的機器人"


class Main(Cog_Extension):
    @app_commands.command(name="ping", description="查看機器人延遲")
    async def ping(self, interaction: discord.Interaction):
        embed = discord.Embed(title=BOT_DISPLAY_NAME, description="Ping值", color=0x28D252)
        embed.add_field(name="目前 Ping 值", value=f"{round(self.bot.latency * 1000)} 毫秒(ms)", inline=True)
        await respond(interaction, embed=embed, ephemeral=True)

    @app_commands.command(name="kick", description="踢出指定成員")
    @app_commands.describe(member="要踢出的成員", reason="原因")
    @app_commands.guild_only()
    @app_commands.default_permissions(kick_members=True)
    async def kick(self, interaction: discord.Interaction, member: discord.Member, reason: str | None = None):
        await member.kick(reason=reason)
        Loggee(f"《指令》〔{interaction.user}〕 踢出 {member}，原因: {reason or '未提供'}")
        await respond(interaction, f"使用者 **{member}** 已被踢出", ephemeral=True)

    @app_commands.command(name="ban", description="封鎖指定成員")
    @app_commands.describe(member="要封鎖的成員", reason="原因")
    @app_commands.guild_only()
    @app_commands.default_permissions(ban_members=True)
    async def ban(self, interaction: discord.Interaction, member: discord.Member, reason: str | None = None):
        await member.ban(reason=reason)
        Loggee(f"《指令》〔{interaction.user}〕 封鎖 {member}，原因: {reason or '未提供'}")
        await respond(interaction, f"使用者 **{member}** 已被封鎖", ephemeral=True)

    @app_commands.command(name="unban", description="解除封鎖指定使用者")
    @app_commands.describe(user="使用者 ID 或舊格式 name#0000")
    @app_commands.guild_only()
    @app_commands.default_permissions(ban_members=True)
    async def unban(self, interaction: discord.Interaction, user: str):
        target_id = int_or_none(user)

        async for ban_entry in interaction.guild.bans(limit=None):
            banned_user = ban_entry.user
            matches_id = target_id is not None and banned_user.id == target_id
            matches_tag = str(banned_user) == user
            if matches_id or matches_tag:
                await interaction.guild.unban(banned_user)
                Loggee(f"《指令》〔{interaction.user}〕 解除封鎖 {banned_user}")
                await respond(interaction, f"使用者 **{banned_user}** 已經解除封鎖", ephemeral=True)
                return

        await respond(interaction, "找不到這位被封鎖的使用者。", ephemeral=True)

    @app_commands.command(name="rename", description="更改指定成員暱稱")
    @app_commands.describe(member="要更名的成員", name="新暱稱")
    @app_commands.guild_only()
    @app_commands.default_permissions(manage_nicknames=True)
    async def rename(self, interaction: discord.Interaction, member: discord.Member, name: str):
        if self.bot.user and member.id == self.bot.user.id and not await self.bot.is_owner(interaction.user):
            await respond(interaction, f"『想幹嘛阿』**{interaction.user.mention}** 想幹嘛阿!", ephemeral=True)
            return

        before = member.display_name
        await member.edit(nick=name)
        await respond(interaction, f"『更改名稱』**{before}** 的暱稱已被變更為: **{name}**", ephemeral=True)

    @app_commands.command(name="nick", description="更改自己的伺服器暱稱")
    @app_commands.describe(name="新暱稱")
    @app_commands.guild_only()
    async def nick(self, interaction: discord.Interaction, name: str):
        member = interaction.user
        before = member.display_name
        await member.edit(nick=name)

        embed = discord.Embed(title=f"『更改 {member.name} 名稱』", color=0xD08A2B)
        embed.set_thumbnail(url=avatar_url(member))
        embed.add_field(name="更改前的名稱", value=before, inline=True)
        embed.add_field(name="更改後的名稱", value=name, inline=False)
        embed.set_footer(text=f"此指令由 {member} 輸入", icon_url=avatar_url(member))
        await respond(interaction, embed=embed, ephemeral=True)

    @app_commands.command(name="avatar", description="顯示使用者頭像")
    @app_commands.describe(member="要查看的成員，留空則查看自己")
    async def avatar(self, interaction: discord.Interaction, member: discord.Member | None = None):
        member = member or interaction.user
        url = avatar_url(member)

        embed = discord.Embed(title=str(member), description=f"[點此到達頭像連結]({url})", color=0xD08A2B)
        embed.set_image(url=url)
        embed.set_footer(text=f"此指令由 {interaction.user} 輸入", icon_url=avatar_url(interaction.user))
        await respond(interaction, embed=embed, ephemeral=True)


async def setup(bot):
    await bot.add_cog(Main(bot))
