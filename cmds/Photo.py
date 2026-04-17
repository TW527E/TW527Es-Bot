import random
import re
from datetime import datetime

import discord
from discord.ext import commands

from core.classes import Cog_Extension
from core.config import ROOT, get_configured_images, get_settings
from core.discord_helpers import delete_invocation
from core.loggee import Loggee


SAFE_FILENAME = re.compile(r"^[A-Za-z0-9_-]+$")


class Photo(Cog_Extension):
    @commands.command()
    async def get_user_icon(self, ctx, member: discord.Member = None):
        await delete_invocation(ctx)
        member = member or ctx.author
        target_dir = ROOT / "downloads" / "avatars"
        target_dir.mkdir(parents=True, exist_ok=True)
        path = target_dir / f"{member.id}-{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
        await member.display_avatar.save(path)
        Loggee(f"『指令』〔{ctx.author}〕 下載 {member} 的頭像到 {path}")
        await ctx.send(f"已下載 {member.mention} 的頭像。")

    @commands.command()
    async def MC(self, ctx):
        await delete_invocation(ctx)
        images = get_configured_images(get_settings(), "MC_img", "Photo")
        if not images:
            await ctx.send("目前沒有可傳送的本機圖片。")
            return
        await ctx.send(file=discord.File(random.choice(images)))

    @commands.command()
    async def url_img(self, ctx):
        await delete_invocation(ctx)
        urls = [url for url in get_settings().get("url_img", []) if isinstance(url, str) and url.startswith("http")]
        if not urls:
            await ctx.send("目前沒有設定可傳送的網路圖片。")
            return
        await ctx.send(random.choice(urls))

    @commands.command(name="G")
    async def send_g_image(self, ctx, filename):
        await delete_invocation(ctx)
        if not SAFE_FILENAME.fullmatch(filename):
            await ctx.send("檔名只能包含英文、數字、底線或連字號。")
            return

        path = ROOT / "G" / f"{filename}.png"
        if not path.exists():
            await ctx.send("找不到這張圖片。")
            return

        await ctx.send(file=discord.File(path))


async def setup(bot):
    await bot.add_cog(Photo(bot))
