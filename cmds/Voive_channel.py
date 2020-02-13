#導入 模組
import discord  #導入Discord.py的專案
from discord.ext import commands  #導入指令
from core.classes import Cog_Extension #導入Cog_extension 的定義
import os

class Voice_channel(Cog_Extension):
    
    @commands.command()
    async def join(self, ctx):
        await ctx.author.voice.channel.connect()

    @commands.command()
    async def leave(self, ctx):
        await ctx.author.voice.channel.disconnect()


def setup(bot):
    bot.add_cog(Voice_channel(bot))