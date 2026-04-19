from datetime import datetime

import discord
from discord import app_commands
from discord.ext import commands, tasks

from core.classes import Cog_Extension
from core.config import get_settings, int_or_none, save_settings
from core.interactions import respond
from core.loggee import Loggee


class Time_message(Cog_Extension):
    def __init__(self, bot):
        super().__init__(bot)
        self.last_sent_date = None
        self.announcement_loop.start()

    def cog_unload(self):
        self.announcement_loop.cancel()

    @tasks.loop(seconds=60)
    async def announcement_loop(self):
        settings = get_settings()
        configured_time = str(settings.get("time", "")).zfill(4)
        now = datetime.now()

        if now.strftime("%H%M") != configured_time:
            return
        if self.last_sent_date == now.date():
            return

        channel_id = int_or_none(settings.get("auto_message_channel")) or int_or_none(settings.get("bot_ready_channel"))
        channel = self.bot.get_channel(channel_id) if channel_id else None
        if channel is None:
            return

        await channel.send(str(settings.get("auto_message") or "test"))
        self.last_sent_date = now.date()
        Loggee(f"自動公告已送出到 {channel}")

    @announcement_loop.before_loop
    async def before_announcement_loop(self):
        await self.bot.wait_until_ready()

    @app_commands.command(name="set_auto_time", description="設定自動公告時間")
    @app_commands.describe(time_text="HHMM 或 HH:MM，例如 0900 或 21:30")
    @app_commands.default_permissions(administrator=True)
    async def set_auto_time(self, interaction: discord.Interaction, time_text: str):
        cleaned = time_text.replace(":", "").strip()
        if len(cleaned) != 4 or not cleaned.isdigit():
            await respond(interaction, "『公告設定』請使用 HHMM 或 HH:MM 格式，例如 0900 或 21:30。", ephemeral=True)
            return

        hour = int(cleaned[:2])
        minute = int(cleaned[2:])
        if hour > 23 or minute > 59:
            await respond(interaction, "『公告設定』時間範圍錯誤。", ephemeral=True)
            return

        save_settings({"time": cleaned})
        self.last_sent_date = None
        await respond(interaction, f"『公告設定』自動公告發送時間已設定為 {cleaned[:2]}:{cleaned[2:]}", ephemeral=True)

    @app_commands.command(name="set_auto_ch", description="設定自動公告頻道")
    @app_commands.describe(channel="公告頻道，留空則使用目前頻道")
    @app_commands.guild_only()
    @app_commands.default_permissions(administrator=True)
    async def set_auto_ch(self, interaction: discord.Interaction, channel: discord.TextChannel | None = None):
        channel = channel or interaction.channel
        if not isinstance(channel, discord.TextChannel):
            await respond(interaction, "『公告設定』請選擇文字頻道。", ephemeral=True)
            return

        save_settings({"auto_message_channel": str(channel.id)})
        await respond(interaction, f"『公告設定』自動公告頻道已設定為 {channel.mention}", ephemeral=True)

    @app_commands.command(name="set_auto_msg", description="設定自動公告內容")
    @app_commands.describe(message="公告內容")
    @app_commands.default_permissions(administrator=True)
    async def set_auto_msg(self, interaction: discord.Interaction, message: str):
        save_settings({"auto_message": message})
        await respond(interaction, "『公告設定』自動公告內容已更新。", ephemeral=True)

    @app_commands.command(name="abc", description="顯示目前 HHMM 時間")
    async def abc(self, interaction: discord.Interaction):
        await respond(interaction, datetime.now().strftime("%H%M"), ephemeral=True)


async def setup(bot):
    await bot.add_cog(Time_message(bot))
