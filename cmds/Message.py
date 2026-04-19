from datetime import datetime

import discord
from discord import app_commands
from discord.ext import commands

from core.classes import Cog_Extension
from core.discord_helpers import avatar_url
from core.interactions import defer, respond
from core.loggee import Loggee


class Message(Cog_Extension):
    @app_commands.command(name="say_msg", description="讓機器人公開傳送指定訊息")
    @app_commands.describe(msg="要讓機器人傳送的訊息")
    @app_commands.default_permissions(administrator=True)
    async def say_msg(self, interaction: discord.Interaction, msg: str):
        Loggee(f"【指令】{interaction.user} 讓機器人複誦訊息")
        await respond(interaction, msg, ephemeral=False)

    @app_commands.command(name="del_msg", description="刪除目前頻道最近的訊息")
    @app_commands.describe(num="刪除數量，最多 100")
    @app_commands.guild_only()
    @app_commands.default_permissions(manage_messages=True)
    async def del_msg(self, interaction: discord.Interaction, num: int):
        await defer(interaction, ephemeral=True)
        deleted = await interaction.channel.purge(limit=max(0, min(num, 100)))
        Loggee(f"【指令】{interaction.user} 刪除 {len(deleted)} 則訊息")
        await interaction.followup.send(f"已刪除 {len(deleted)} 則訊息。", ephemeral=True)

    @app_commands.command(name="say_dm", description="傳送私訊給指定成員")
    @app_commands.describe(member="要接收私訊的成員", msg="要傳送的訊息")
    @app_commands.guild_only()
    @app_commands.default_permissions(administrator=True)
    async def say_dm(self, interaction: discord.Interaction, member: discord.Member, msg: str):
        await member.send(msg)

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        embed = discord.Embed(title="『私訊聊天室』", color=0xD08A2B)
        embed.set_thumbnail(url=avatar_url(member))
        embed.add_field(name="指定使用者", value=member.mention, inline=True)
        embed.add_field(name="指定的訊息", value=msg[:1024], inline=False)
        embed.set_footer(text=f"此指令由 {interaction.user} 輸入 • {now}", icon_url=avatar_url(interaction.user))
        await respond(interaction, embed=embed, ephemeral=True)

    @app_commands.command(name="now_time", description="查看機器人目前時間")
    async def now_time(self, interaction: discord.Interaction):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        await respond(interaction, f"現在機器人的時間是 {now}", ephemeral=True)


async def setup(bot):
    await bot.add_cog(Message(bot))
