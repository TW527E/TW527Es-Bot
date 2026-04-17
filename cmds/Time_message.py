from datetime import datetime

from discord.ext import commands, tasks

from core.classes import Cog_Extension
from core.config import get_settings, int_or_none, save_settings
from core.discord_helpers import delete_invocation
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

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def set_auto_time(self, ctx, time_text):
        await delete_invocation(ctx)
        cleaned = time_text.replace(":", "").strip()
        if len(cleaned) != 4 or not cleaned.isdigit():
            await ctx.send("『公告設定』請使用 HHMM 或 HH:MM 格式，例如 0900 或 21:30。")
            return

        hour = int(cleaned[:2])
        minute = int(cleaned[2:])
        if hour > 23 or minute > 59:
            await ctx.send("『公告設定』時間範圍錯誤。")
            return

        save_settings({"time": cleaned})
        self.last_sent_date = None
        await ctx.send(f"『公告設定』自動公告發送時間已設定為 {cleaned[:2]}:{cleaned[2:]}")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def set_auto_ch(self, ctx, channel_id: int = None):
        await delete_invocation(ctx)
        channel_id = channel_id or ctx.channel.id
        channel = self.bot.get_channel(channel_id)
        if channel is None:
            await ctx.send("『公告設定』找不到這個頻道。")
            return

        save_settings({"auto_message_channel": str(channel_id)})
        await ctx.send(f"『公告設定』自動公告頻道已設定為 {channel.mention}")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def set_auto_msg(self, ctx, *, message):
        await delete_invocation(ctx)
        save_settings({"auto_message": message})
        await ctx.send("『公告設定』自動公告內容已更新。")

    @commands.command()
    async def abc(self, ctx):
        await ctx.send(datetime.now().strftime("%H%M"))


async def setup(bot):
    await bot.add_cog(Time_message(bot))
