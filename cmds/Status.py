import discord
from discord import app_commands
from discord.ext import commands

from core.classes import Cog_Extension
from core.interactions import owner_only, respond
from core.loggee import Loggee


class Status(Cog_Extension):
    @app_commands.command(name="shutdown", description="關閉機器人")
    @owner_only()
    async def shutdown(self, interaction: discord.Interaction):
        Loggee(f"『指令』〔{interaction.user}〕 輸入 [shutdown - 機器人關機] 指令")
        await respond(interaction, "【狀態】掰掰 我已關機", ephemeral=True)
        await self.bot.close()

    @app_commands.command(name="online", description="將機器人狀態設為線上")
    @owner_only()
    async def online(self, interaction: discord.Interaction):
        await self.bot.change_presence(
            status=discord.Status.online,
            activity=discord.Activity(type=discord.ActivityType.watching, name="我現在不知道要幹嘛...."),
        )
        await respond(interaction, "【狀態】你好 我已經啟動!", ephemeral=True)

    @app_commands.command(name="idle", description="將機器人狀態設為閒置")
    @owner_only()
    async def idle(self, interaction: discord.Interaction):
        await self.bot.change_presence(
            status=discord.Status.idle,
            activity=discord.Activity(type=discord.ActivityType.watching, name="ψ(｀∇´)ψ"),
        )
        await respond(interaction, "【狀態】我太懶了 不想做事!", ephemeral=True)

    @app_commands.command(name="dnd", description="將機器人狀態設為請勿打擾")
    @owner_only()
    async def dnd(self, interaction: discord.Interaction):
        await self.bot.change_presence(
            status=discord.Status.dnd,
            activity=discord.Activity(type=discord.ActivityType.watching, name="不要吵我"),
        )
        await respond(interaction, "【狀態】不要打擾我", ephemeral=True)

    @app_commands.command(name="inv", description="將機器人狀態設為隱形")
    @owner_only()
    async def inv(self, interaction: discord.Interaction):
        await self.bot.change_presence(status=discord.Status.invisible)
        await respond(interaction, "【狀態】已切換為隱形", ephemeral=True)

    @app_commands.command(name="test", description="將機器人狀態設為測試中")
    @owner_only()
    async def test(self, interaction: discord.Interaction):
        await self.bot.change_presence(
            status=discord.Status.dnd,
            activity=discord.Activity(type=discord.ActivityType.watching, name="機器人測試中"),
        )
        await respond(interaction, "【狀態】機器人測試中 請勿打擾", ephemeral=True)

    @app_commands.command(name="status", description="自訂機器人狀態")
    @app_commands.describe(state="online、idle 或 dnd", name="狀態文字")
    @app_commands.choices(
        state=[
            app_commands.Choice(name="線上", value="online"),
            app_commands.Choice(name="閒置", value="idle"),
            app_commands.Choice(name="請勿打擾", value="dnd"),
        ]
    )
    @owner_only()
    async def status(self, interaction: discord.Interaction, state: app_commands.Choice[str], name: str | None = None):
        name = name or "ヾ(•ω•`)o"
        states = {
            "online": (discord.Status.online, "線上"),
            "idle": (discord.Status.idle, "閒置"),
            "dnd": (discord.Status.dnd, "請勿打擾"),
        }
        discord_status, label = states[state.value]
        await self.bot.change_presence(
            status=discord_status,
            activity=discord.Activity(type=discord.ActivityType.watching, name=name),
        )
        await respond(interaction, f"【狀態】目前狀態:{label} 目前狀態消息:{name}", ephemeral=True)


async def setup(bot):
    await bot.add_cog(Status(bot))
