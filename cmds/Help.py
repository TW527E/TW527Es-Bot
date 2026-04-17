import discord
from discord.ext import commands

from core.classes import Cog_Extension
from core.config import get_settings
from core.discord_helpers import delete_invocation


class Help(Cog_Extension):
    @commands.command(name="help")
    async def help_command(self, ctx, category=None):
        await delete_invocation(ctx)
        prefix = get_settings().get("prefix", "|")

        pages = {
            None: [
                ("基本", f"`{prefix}ping`, `{prefix}avatar`, `{prefix}info`, `{prefix}guild`, `{prefix}level`"),
                ("管理", f"`{prefix}kick`, `{prefix}ban`, `{prefix}unban`, `{prefix}del_msg`, `{prefix}say_msg`, `{prefix}vote`"),
                ("伺服器", f"`{prefix}add_text_ch`, `{prefix}add_voice_ch`, `{prefix}roles`, `{prefix}add_role`, `{prefix}remove_role`"),
                ("Owner", f"`{prefix}invite`, `{prefix}load`, `{prefix}unload`, `{prefix}reload`, `{prefix}reload_all`, `{prefix}status`"),
            ],
            "basic": [
                ("一般指令", f"`{prefix}ping` 延遲\n`{prefix}avatar [@使用者]` 頭像\n`{prefix}info [@使用者]` 使用者資訊\n`{prefix}guild` 伺服器資訊\n`{prefix}now_time` 現在時間"),
                ("圖片", f"`{prefix}MC` 隨機本機 Minecraft 圖片\n`{prefix}url_img` 隨機網路圖片\n`{prefix}G <檔名>` 傳送 G 資料夾圖片"),
            ],
            "admin": [
                ("管理指令", f"`{prefix}kick @使用者 [原因]`\n`{prefix}ban @使用者 [原因]`\n`{prefix}unban 使用者#0000`\n`{prefix}del_msg 數量`\n`{prefix}say_msg 訊息`\n`{prefix}say_dm @使用者 訊息`"),
                ("伺服器指令", f"`{prefix}add_text_ch 名稱`\n`{prefix}add_voice_ch 名稱`\n`{prefix}add_role @使用者 @身分組`\n`{prefix}remove_role @使用者 @身分組`"),
            ],
        }

        key = category.lower() if isinstance(category, str) else None
        fields = pages.get(key)
        if fields is None:
            await ctx.send("『指令提示幫助』找不到這個分類。可用分類: basic, admin")
            return

        embed = discord.Embed(title="TaiwanMC-苦力怕同學", description="指令提示幫助", color=0x28D252)
        for name, value in fields:
            embed.add_field(name=name, value=value, inline=False)
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Help(bot))
