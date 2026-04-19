import logging

import discord
from discord import app_commands
from discord.ext import commands

from core.config import get_guild_configs, get_owner_id, get_settings, get_token, int_or_none
from core.interactions import owner_only, respond
from core.loggee import Loggee


EXTENSION_DIRS = ("cmds", "event", "server")
BOT_DISPLAY_NAME = "TW527E的機器人"


def iter_extensions():
    from core.config import ROOT

    for folder in EXTENSION_DIRS:
        directory = ROOT / folder
        if not directory.exists():
            continue
        for path in sorted(directory.glob("*.py")):
            if path.name.startswith("_"):
                continue
            yield f"{folder}.{path.stem}"


class TW527EBot(commands.Bot):
    def __init__(self):
        self.settings = get_settings()
        self._ready_announced = False

        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        intents.reactions = True

        super().__init__(
            command_prefix=commands.when_mentioned,
            help_command=None,
            intents=intents,
            owner_id=get_owner_id(self.settings),
        )
        self.tree.on_error = self.on_app_command_error

    async def setup_hook(self):
        for extension in iter_extensions():
            try:
                await self.load_extension(extension)
                Loggee(f"已載入插件 {extension}")
            except Exception as exc:
                Loggee(f"載入插件 {extension} 失敗: {exc}")

        await self.sync_application_commands()

    async def sync_application_commands(self):
        guild_configs = get_guild_configs()
        if guild_configs:
            for config in guild_configs:
                guild = discord.Object(id=config["guild_id"])
                self.tree.copy_global_to(guild=guild)
                synced = await self.tree.sync(guild=guild)
                Loggee(f"已同步 {len(synced)} 個斜線指令到 guild {config['guild_id']}")
            return

        synced = await self.tree.sync()
        Loggee(f"已同步 {len(synced)} 個全域斜線指令")

    async def on_ready(self):
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name="/help 獲取指令提示幫助",
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

    async def on_app_command_error(self, interaction, error):
        original = getattr(error, "original", error)

        if isinstance(original, app_commands.MissingPermissions):
            await respond(interaction, "【錯誤】你沒有執行這個指令的權限。", ephemeral=True)
            return
        if isinstance(original, app_commands.CheckFailure):
            await respond(interaction, "【錯誤】這個指令只有機器人擁有者可以使用。", ephemeral=True)
            return
        if isinstance(original, app_commands.NoPrivateMessage):
            await respond(interaction, "【錯誤】這個指令只能在伺服器內使用。", ephemeral=True)
            return
        if isinstance(original, discord.Forbidden):
            await respond(interaction, "【錯誤】我缺少執行這個操作需要的 Discord 權限。", ephemeral=True)
            return

        Loggee(f"斜線指令錯誤: {type(original).__name__}: {original}")
        await respond(interaction, "【錯誤】指令執行時發生問題，已寫入 Log。", ephemeral=True)


bot = TW527EBot()


@bot.tree.command(name="logout", description="關閉機器人")
@owner_only()
async def logout(interaction: discord.Interaction):
    Loggee(f"『{interaction.user}』 輸入 機器人關機 Shutdown")
    await respond(interaction, "『登出』登登登登 (XP登出)", ephemeral=True)
    await bot.close()


@bot.tree.command(name="guild_leave", description="讓機器人離開指定伺服器")
@app_commands.describe(guild_id="伺服器 ID")
@owner_only()
async def guild_leave(interaction: discord.Interaction, guild_id: str):
    guild = bot.get_guild(int(guild_id))
    if guild is None:
        await respond(interaction, "找不到這個伺服器。", ephemeral=True)
        return

    guild_name = guild.name
    await guild.leave()
    Loggee(f"『{interaction.user}』 讓機器人離開 {guild_name}")
    await respond(interaction, f"已離開 {guild_name}", ephemeral=True)


@bot.tree.command(name="bot_guild", description="列出機器人目前所在伺服器")
@owner_only()
async def bot_guild(interaction: discord.Interaction):
    guild_names = "\n".join(f"{guild.name} ({guild.id})" for guild in bot.guilds)
    await respond(interaction, guild_names or "目前不在任何伺服器。", ephemeral=True)


@bot.tree.command(name="guild_invite", description="建立指定伺服器的邀請連結")
@app_commands.describe(guild_id="伺服器 ID")
@owner_only()
async def guild_invite(interaction: discord.Interaction, guild_id: str):
    guild = bot.get_guild(int(guild_id))
    if guild is None:
        await respond(interaction, "找不到這個伺服器。", ephemeral=True)
        return

    me = guild.me or (guild.get_member(bot.user.id) if bot.user else None)
    if me is None:
        await respond(interaction, "無法確認機器人在該伺服器的權限。", ephemeral=True)
        return

    channel = next((ch for ch in guild.text_channels if ch.permissions_for(me).create_instant_invite), None)
    if channel is None:
        await respond(interaction, "找不到可以建立邀請連結的文字頻道。", ephemeral=True)
        return

    invite = await channel.create_invite(max_age=0, max_uses=0, reason=f"{interaction.user} requested invite")
    await respond(interaction, str(invite), ephemeral=True)


@bot.tree.command(name="invite", description="取得機器人邀請連結")
@owner_only()
async def invite(interaction: discord.Interaction):
    if bot.user is None:
        await respond(interaction, "機器人尚未登入。", ephemeral=True)
        return

    permissions = discord.Permissions(administrator=True)
    url = discord.utils.oauth_url(bot.user.id, permissions=permissions, scopes=("bot", "applications.commands"))
    await respond(interaction, f"機器人的邀請碼: {url}", ephemeral=True)


@bot.tree.command(name="load", description="載入 extension")
@app_commands.describe(extension="例如 cmds.Main")
@owner_only()
async def load(interaction: discord.Interaction, extension: str):
    await bot.load_extension(extension)
    await bot.sync_application_commands()
    await respond(interaction, f"載入 **{extension}** 完成!", ephemeral=True)


@bot.tree.command(name="unload", description="卸載 extension")
@app_commands.describe(extension="例如 cmds.Main")
@owner_only()
async def unload(interaction: discord.Interaction, extension: str):
    await bot.unload_extension(extension)
    await bot.sync_application_commands()
    await respond(interaction, f"卸載 **{extension}** 完成!", ephemeral=True)


@bot.tree.command(name="reload", description="重新載入 extension")
@app_commands.describe(extension="例如 cmds.Main")
@owner_only()
async def reload_extension(interaction: discord.Interaction, extension: str):
    await bot.reload_extension(extension)
    await bot.sync_application_commands()
    await respond(interaction, f"重新載入 **{extension}** 完成!", ephemeral=True)


@bot.tree.command(name="reload_all", description="重新載入所有 extension")
@owner_only()
async def reload_all(interaction: discord.Interaction):
    for extension in list(bot.extensions):
        await bot.reload_extension(extension)
    await bot.sync_application_commands()
    await respond(interaction, "重新載入 **全部** 完成!", ephemeral=True)


def main():
    logging.basicConfig(level=logging.INFO)
    token = get_token(bot.settings)
    if not token:
        raise RuntimeError("找不到 Discord token。請在 .env 設定 DISCORD_TOKEN，或在本機 setting.json 設定 Token。")

    bot.run(token)


if __name__ == "__main__":
    main()
