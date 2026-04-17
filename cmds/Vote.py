import discord
from discord.ext import commands

from core.classes import Cog_Extension
from core.discord_helpers import delete_invocation


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
    @commands.command()
    async def vote(self, ctx, title, *, vote):
        await delete_invocation(ctx)
        options = [item.strip() for item in vote.split("=") if item.strip()]
        if not options:
            await ctx.send("請至少提供一個投票選項，例如 `|vote 晚餐 拉麵=火鍋`。")
            return
        if len(options) > len(VOTE_EMOJIS):
            await ctx.send(f"最多只能提供 {len(VOTE_EMOJIS)} 個選項。")
            return

        embed = discord.Embed(title=title, description="投票", color=0x28D252)
        for emoji, option in zip(VOTE_EMOJIS, options):
            embed.add_field(name=f"反應 {emoji}", value=option, inline=False)

        message = await ctx.send(embed=embed)
        for emoji in VOTE_EMOJIS[: len(options)]:
            await message.add_reaction(emoji)


async def setup(bot):
    await bot.add_cog(Vote(bot))
