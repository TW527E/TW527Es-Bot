import discord
from discord import app_commands
from discord.ext import commands

from core.classes import Cog_Extension
from core.discord_helpers import avatar_url, guild_icon_url
from core.interactions import chunk_values, respond
from core.loggee import Loggee


class Server(Cog_Extension):
    @app_commands.command(name="set_server_name", description="修改伺服器名稱")
    @app_commands.describe(name="新的伺服器名稱")
    @app_commands.guild_only()
    @app_commands.default_permissions(administrator=True)
    async def set_server_name(self, interaction: discord.Interaction, name: str):
        before = interaction.guild.name
        await interaction.guild.edit(name=name, reason=f"{interaction.user} changed server name")

        icon = guild_icon_url(interaction.guild)
        embed = discord.Embed(title="『指令-更改伺服器名稱』", color=0xD08A2B)
        if icon:
            embed.description = f"[點此到達伺服器頭像連結]({icon})"
            embed.set_thumbnail(url=icon)
        embed.add_field(name="更改前的伺服器名稱", value=before, inline=True)
        embed.add_field(name="更改後的伺服器名稱", value=name, inline=False)
        embed.set_footer(text=f"此指令由 {interaction.user} 輸入", icon_url=avatar_url(interaction.user))
        Loggee(f"『指令-更改伺服器名稱』 {interaction.user.name} 在 {before} 修改伺服器名稱為 {name}")
        await respond(interaction, embed=embed, ephemeral=True)

    @app_commands.command(name="add_role", description="增加使用者身分組")
    @app_commands.describe(member="要增加身分組的成員", role="要增加的身分組")
    @app_commands.guild_only()
    @app_commands.default_permissions(manage_roles=True)
    async def add_role(self, interaction: discord.Interaction, member: discord.Member, role: discord.Role):
        await member.add_roles(role, reason=f"{interaction.user} used add_role")
        await self._send_role_embed(interaction, "增加使用者身分組", member, role)

    @app_commands.command(name="remove_role", description="移除使用者身分組")
    @app_commands.describe(member="要移除身分組的成員", role="要移除的身分組")
    @app_commands.guild_only()
    @app_commands.default_permissions(manage_roles=True)
    async def remove_role(self, interaction: discord.Interaction, member: discord.Member, role: discord.Role):
        await member.remove_roles(role, reason=f"{interaction.user} used remove_role")
        await self._send_role_embed(interaction, "刪除使用者身分組", member, role)

    @app_commands.command(name="create_role", description="建立身分組")
    @app_commands.describe(name="身分組名稱")
    @app_commands.guild_only()
    @app_commands.default_permissions(manage_roles=True)
    async def create_role(self, interaction: discord.Interaction, name: str):
        role = await interaction.guild.create_role(name=name, reason=f"{interaction.user} created role")
        await respond(interaction, f"已建立身分組 {role.mention}", ephemeral=True)

    @app_commands.command(name="roles", description="列出伺服器身分組")
    @app_commands.guild_only()
    async def roles(self, interaction: discord.Interaction):
        roles = [role.mention for role in interaction.guild.roles if role.name != "@everyone"]
        embed = discord.Embed(title="『群內所有身分組』", description="群內所有身分組", color=0xD08A2B)
        icon = guild_icon_url(interaction.guild)
        if icon:
            embed.set_thumbnail(url=icon)
        embed.add_field(name="群組", value=interaction.guild.name[:1024], inline=True)
        for index, chunk in enumerate(chunk_values(roles), start=1):
            name = "身分組" if index == 1 else f"身分組 {index}"
            embed.add_field(name=name, value=chunk, inline=False)
        embed.set_footer(text=f"此指令由 {interaction.user} 輸入", icon_url=avatar_url(interaction.user))
        await respond(interaction, embed=embed, ephemeral=True)

    async def _send_role_embed(self, interaction, title, member, role):
        embed = discord.Embed(title=f"『{title}』", color=0xD08A2B)
        embed.set_thumbnail(url=avatar_url(member))
        embed.add_field(name="使用者", value=member.mention, inline=True)
        embed.add_field(name="身分組", value=role.mention, inline=False)
        embed.set_footer(text=f"此指令由 {interaction.user} 輸入", icon_url=avatar_url(interaction.user))
        Loggee(f"『{title}』 {interaction.user.name} 在 {interaction.guild.name} 對 {member} 操作 {role}")
        await respond(interaction, embed=embed, ephemeral=True)


async def setup(bot):
    await bot.add_cog(Server(bot))
