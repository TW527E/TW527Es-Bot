import discord
from discord import app_commands
from discord.ext import commands

from core.classes import Cog_Extension
from core.interactions import respond


BOT_DISPLAY_NAME = "TW527E的機器人"


class Help(Cog_Extension):
    @app_commands.command(name="help", description="查看指令提示")
    @app_commands.describe(category="分類：basic 或 admin")
    async def help_command(self, interaction: discord.Interaction, category: str | None = None):
        pages = {
            None: [
                ("基本", "`/ping`, `/avatar`, `/info`, `/guild`, `/level`, `/now_time`"),
                ("管理", "`/kick`, `/ban`, `/unban`, `/del_msg`, `/say_msg`, `/vote`"),
                ("伺服器", "`/add_text_ch`, `/add_voice_ch`, `/roles`, `/add_role`, `/remove_role`"),
                ("Owner", "`/invite`, `/load`, `/unload`, `/reload`, `/reload_all`, `/status`"),
            ],
            "basic": [
                ("一般指令", "`/ping` 延遲\n`/avatar` 頭像\n`/info` 使用者資訊\n`/guild` 伺服器資訊\n`/now_time` 現在時間"),
                ("圖片", "`/mc` 隨機本機 Minecraft 圖片\n`/url_img` 隨機網路圖片\n`/g` 傳送 G 資料夾圖片"),
            ],
            "admin": [
                ("管理指令", "`/kick`\n`/ban`\n`/unban`\n`/del_msg`\n`/say_msg`\n`/say_dm`"),
                ("伺服器指令", "`/add_text_ch`\n`/add_voice_ch`\n`/add_role`\n`/remove_role`\n`/create_role`"),
            ],
        }

        key = category.lower() if isinstance(category, str) else None
        fields = pages.get(key)
        if fields is None:
            await respond(interaction, "『指令提示幫助』找不到這個分類。可用分類: basic, admin", ephemeral=True)
            return

        embed = discord.Embed(title=BOT_DISPLAY_NAME, description="指令提示幫助", color=0x28D252)
        for name, value in fields:
            embed.add_field(name=name, value=value, inline=False)
        await respond(interaction, embed=embed, ephemeral=True)


async def setup(bot):
    await bot.add_cog(Help(bot))
