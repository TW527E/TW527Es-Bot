import discord
from discord import app_commands
from discord.ext import commands

from core.classes import Cog_Extension
from core.interactions import respond


class Channel(Cog_Extension):
    @app_commands.command(name="add_text_ch", description="建立文字頻道")
    @app_commands.describe(name="頻道名稱")
    @app_commands.guild_only()
    @app_commands.default_permissions(manage_channels=True)
    async def add_text_ch(self, interaction: discord.Interaction, name: str):
        channel = await interaction.guild.create_text_channel(name, reason=f"{interaction.user} created by command")
        await respond(interaction, f"《文字頻道》已建立 {channel.mention}", ephemeral=True)

    @app_commands.command(name="add_voice_ch", description="建立語音頻道")
    @app_commands.describe(name="頻道名稱")
    @app_commands.guild_only()
    @app_commands.default_permissions(manage_channels=True)
    async def add_voice_ch(self, interaction: discord.Interaction, name: str):
        channel = await interaction.guild.create_voice_channel(name, reason=f"{interaction.user} created by command")
        await respond(interaction, f"《語音頻道》已建立 **{channel.name}**", ephemeral=True)


async def setup(bot):
    await bot.add_cog(Channel(bot))
