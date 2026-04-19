import discord
from discord import app_commands
from discord.ext import commands

from core.classes import Cog_Extension
from core.interactions import respond


VOTE_EMOJIS = [
    "🇦",
    "🇧",
    "🇨",
    "🇩",
    "🇪",
    "🇫",
    "🇬",
    "🇭",
    "🇮",
    "🇯",
    "🇰",
    "🇱",
    "🇲",
    "🇳",
    "🇴",
    "🇵",
    "🇶",
    "🇷",
    "🇸",
    "🇹",
]


class Vote(Cog_Extension):
    @app_commands.command(name="vote", description="建立公開投票")
    @app_commands.describe(title="投票標題", options="使用 = 分隔選項，例如 拉麵=火鍋")
    async def vote(self, interaction: discord.Interaction, title: str, options: str):
        choices = [item.strip() for item in options.split("=") if item.strip()]
        if not choices:
            await respond(interaction, "請至少提供一個投票選項，例如 `/vote title:晚餐 options:拉麵=火鍋`。", ephemeral=True)
            return
        if len(choices) > len(VOTE_EMOJIS):
            await respond(interaction, f"最多只能提供 {len(VOTE_EMOJIS)} 個選項。", ephemeral=True)
            return

        embed = discord.Embed(title=title, description="投票", color=0x28D252)
        for emoji, option in zip(VOTE_EMOJIS, choices):
            embed.add_field(name=f"反應 {emoji}", value=option[:1024], inline=False)

        await interaction.response.send_message(embed=embed)
        message = await interaction.original_response()
        for emoji in VOTE_EMOJIS[: len(choices)]:
            await message.add_reaction(emoji)


async def setup(bot):
    await bot.add_cog(Vote(bot))
