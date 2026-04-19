import asyncio
from pathlib import Path

import discord
from discord import app_commands
from discord.ext import commands

from core.classes import Cog_Extension
from core.config import DATA_DIR, ROOT, read_json, write_json
from core.discord_helpers import avatar_url
from core.interactions import respond
from core.loggee import Loggee


LEVELS_PATH = DATA_DIR / "levels.json"
LEGACY_LEVELS_PATH = ROOT / "Level_System.json"


class Level(Cog_Extension):
    def __init__(self, bot):
        super().__init__(bot)
        DATA_DIR.mkdir(exist_ok=True)
        self.users = self._load_users()
        self.save_task = asyncio.create_task(self._save_periodically())

    def cog_unload(self):
        self.save_task.cancel()

    def _load_users(self):
        if LEVELS_PATH.exists():
            return read_json(LEVELS_PATH, {})
        if LEGACY_LEVELS_PATH.exists():
            return read_json(LEGACY_LEVELS_PATH, {})
        return {}

    async def _save_periodically(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            write_json(LEVELS_PATH, self.users)
            await asyncio.sleep(30)

    @staticmethod
    def _needed_exp(level):
        return round((4 * (level * 6)) / 2)

    def _ensure_user(self, member):
        member_id = str(member.id)
        if member_id not in self.users:
            self.users[member_id] = {"level": 1, "exp": 0, "message": 0}
        return member_id

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or message.guild is None:
            return

        author_id = self._ensure_user(message.author)
        data = self.users[author_id]
        data["message"] += 1
        data["exp"] += 1

        if data["exp"] >= self._needed_exp(data["level"]):
            data["level"] += 1
            data["exp"] = 0
            Loggee(f"『等級系統』{message.author} 升等，目前等級為 {data['level']}")
            await message.channel.send(f"『等級系統』**{message.author}** 你升級了，目前等級為 **{data['level']}**")

    @app_commands.command(name="level", description="查看等級資料")
    @app_commands.describe(member="要查看的成員，留空則查看自己")
    @app_commands.guild_only()
    async def level(self, interaction: discord.Interaction, member: discord.Member | None = None):
        member = member or interaction.user
        member_id = self._ensure_user(member)
        data = self.users[member_id]
        needed = self._needed_exp(data["level"]) - data["exp"]

        embed = discord.Embed(title=f"『等級系統』 - {member.display_name}", color=0x28D252)
        embed.set_thumbnail(url=avatar_url(member))
        embed.add_field(name="目前等級", value=str(data["level"]), inline=False)
        embed.add_field(name="經驗值", value=f"還差 {needed} 個經驗才能升級", inline=False)
        embed.add_field(name="打了多少次訊息", value=str(data["message"]), inline=False)
        embed.set_footer(text=f"此指令由 {interaction.user} 輸入", icon_url=avatar_url(interaction.user))
        await respond(interaction, embed=embed, ephemeral=True)


async def setup(bot):
    await bot.add_cog(Level(bot))
