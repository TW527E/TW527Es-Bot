import random
import re
from datetime import datetime

import discord
from discord import app_commands
from discord.ext import commands

from core.classes import Cog_Extension
from core.config import ROOT, get_configured_images, get_settings
from core.interactions import respond
from core.loggee import Loggee


SAFE_FILENAME = re.compile(r"^[A-Za-z0-9_-]+$")


class Photo(Cog_Extension):
    @app_commands.command(name="get_user_icon", description="下載指定成員頭像到本機 downloads 資料夾")
    @app_commands.describe(member="要下載頭像的成員，留空則下載自己")
    async def get_user_icon(self, interaction: discord.Interaction, member: discord.Member | None = None):
        member = member or interaction.user
        target_dir = ROOT / "downloads" / "avatars"
        target_dir.mkdir(parents=True, exist_ok=True)
        path = target_dir / f"{member.id}-{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
        await member.display_avatar.save(path)
        Loggee(f"『指令』〔{interaction.user}〕 下載 {member} 的頭像到 {path}")
        await respond(interaction, f"已下載 {member.mention} 的頭像。", ephemeral=True)

    @app_commands.command(name="mc", description="隨機傳送本機 Minecraft 圖片")
    async def mc(self, interaction: discord.Interaction):
        images = get_configured_images(get_settings(), "MC_img", "Photo")
        if not images:
            await respond(interaction, "目前沒有可傳送的本機圖片。", ephemeral=True)
            return
        await respond(interaction, file=discord.File(random.choice(images)), ephemeral=False)

    @app_commands.command(name="url_img", description="隨機傳送設定中的網路圖片 URL")
    async def url_img(self, interaction: discord.Interaction):
        urls = [url for url in get_settings().get("url_img", []) if isinstance(url, str) and url.startswith("http")]
        if not urls:
            await respond(interaction, "目前沒有設定可傳送的網路圖片。", ephemeral=True)
            return
        await respond(interaction, random.choice(urls), ephemeral=False)

    @app_commands.command(name="g", description="傳送 G 資料夾內的指定圖片")
    @app_commands.describe(filename="不含副檔名的圖片檔名")
    async def send_g_image(self, interaction: discord.Interaction, filename: str):
        if not SAFE_FILENAME.fullmatch(filename):
            await respond(interaction, "檔名只能包含英文、數字、底線或連字號。", ephemeral=True)
            return

        path = ROOT / "G" / f"{filename}.png"
        if not path.exists():
            await respond(interaction, "找不到這張圖片。", ephemeral=True)
            return

        await respond(interaction, file=discord.File(path), ephemeral=False)


async def setup(bot):
    await bot.add_cog(Photo(bot))
