import logging
from pathlib import Path

import discord
from discord.ext import commands

from core.config import ROOT, get_owner_id, get_settings, get_token, int_or_none
from core.loggee import Loggee


EXTENSION_DIRS = ("cmds", "event", "server")


def iter_extensions():
    for folder in EXTENSION_DIRS:
        directory = ROOT / folder
        if not directory.exists():
            continue
        for path in sorted(directory.glob("*.py")):
            if path.name.startswith("_"):
                continue
            yield f"{folder}.{path.stem}"


BOT_DISPLAY_NAME = "TW527E的機器人"


class TW527EBot(commands.Bot):
    def __init__(self):
        self.settings = get_settings()
        self._ready_announced = False

        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        intents.reactions = True

        super().__init__(
            command_prefix=str(self.settings.get("prefix", "|")),
            help_command=None,
            intents=intents,
            owner_id=get_owner_id(self.settings),
        )

    async def setup_hook(self):
        for extension in iter_extensions():
            try:
                await self.load_extension(extension)
                Loggee(f"已載入插件 {extension}")
            except Exception as exc:
                Loggee(f"載入插件 {extension} 失敗: {exc}")

    async def on_ready(self):
        prefix = self.command_prefix
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name=f"{prefix}help 獲取指令提示幫助",
            )
        )

        if self._ready_announced:
            return

        self._ready_announced = True
        Loggee("＝＝＝已登入＝＝＝")
        Loggee(f"《 {self.user} 》上線了")
        Loggee(f"目前在的群組有 {[guild.name for guild in self.guilds]}")
        Loggee("＝＝＝已登入＝＝＝")

        channel_id = int_or_none(self.settings.get("bot_ready_channel"))
        if channel_id is None:
            return

        channel = self.get_channel(channel_id)
        if channel is not None:
            await channel.send(f"《 **__{BOT_DISPLAY_NAME}__** 》上線了")

    async def on_command_error(self, ctx, error):
        error = getattr(error, "original", error)

        if isinstance(error, commands.CommandNotFound):
            return
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f"【錯誤】{ctx.author.mention} 你沒有執行這個指令的權限。", delete_after=5)
            return
        if isinstance(error, commands.NotOwner):
            await ctx.send(f"【錯誤】{ctx.author.mention} 這個指令只有機器人擁有者可以使用。", delete_after=5)
            return
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"【錯誤】{ctx.author.mention} 這個指令少了必要參數。", delete_after=5)
            return
        if isinstance(error, commands.BotMissingPermissions):
            await ctx.send("【錯誤】我缺少執行這個操作需要的 Discord 權限。", delete_after=5)
            return

        Loggee(f"指令錯誤: {type(error).__name__}: {error}")
        await ctx.send("【錯誤】指令執行時發生問題，已寫入 Log。", delete_after=5)


bot = TW527EBot()


@bot.command()
@commands.is_owner()
async def logout(ctx):
    Loggee(f"『{ctx.author}』 輸入 機器人關機 Shutdown")
    await ctx.send("『登出』登登登登 (XP登出)")
    await bot.close()


@bot.command()
@commands.is_owner()
async def guild_leave(ctx, guild_id: int):
    guild = bot.get_guild(guild_id)
    if guild is None:
        await ctx.send("找不到這個伺服器。")
        return
    await guild.leave()
    Loggee(f"『{ctx.author}』 讓機器人離開 {guild.name}")
    await ctx.send(f"已離開 {guild.name}")


@bot.command()
@commands.is_owner()
async def bot_guild(ctx):
    guild_names = "\n".join(f"{guild.name} ({guild.id})" for guild in bot.guilds)
    await ctx.send(guild_names or "目前不在任何伺服器。")


@bot.command()
@commands.is_owner()
async def guild_invite(ctx, guild_id: int):
    guild = bot.get_guild(guild_id)
    if guild is None:
        await ctx.send("找不到這個伺服器。")
        return

    me = guild.me or (guild.get_member(bot.user.id) if bot.user else None)
    if me is None:
        await ctx.send("無法確認機器人在該伺服器的權限。")
        return

    channel = next((ch for ch in guild.text_channels if ch.permissions_for(me).create_instant_invite), None)
    if channel is None:
        await ctx.send("找不到可以建立邀請連結的文字頻道。")
        return

    invite = await channel.create_invite(max_age=0, max_uses=0, reason=f"{ctx.author} requested invite")
    await ctx.send(str(invite))


@bot.command()
@commands.is_owner()
async def invite(ctx):
    if bot.user is None:
        await ctx.send("機器人尚未登入。")
        return

    permissions = discord.Permissions(administrator=True)
    url = discord.utils.oauth_url(bot.user.id, permissions=permissions, scopes=("bot", "applications.commands"))
    await ctx.send(f"機器人的邀請碼: {url}")


@bot.command()
@commands.is_owner()
async def load(ctx, extension: str):
    await bot.load_extension(extension)
    await ctx.send(f"載入 **{extension}** 完成!")


@bot.command()
@commands.is_owner()
async def unload(ctx, extension: str):
    await bot.unload_extension(extension)
    await ctx.send(f"卸載 **{extension}** 完成!")


@bot.command()
@commands.is_owner()
async def reload(ctx, extension: str):
    await bot.reload_extension(extension)
    await ctx.send(f"重新載入 **{extension}** 完成!")


@bot.command()
@commands.is_owner()
async def reload_all(ctx):
    for extension in list(bot.extensions):
        await bot.reload_extension(extension)
    await ctx.send("重新載入 **全部** 完成!")


def main():
    logging.basicConfig(level=logging.INFO)
    token = get_token(bot.settings)
    if not token:
        raise RuntimeError(
            "找不到 Discord token。請在 .env 設定 DISCORD_TOKEN，或在本機 setting.json 設定 Token。"
        )

    bot.run(token)


if __name__ == "__main__":
    main()
