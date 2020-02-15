#導入 模組
import discord  #導入Discord.py的專案
from discord.ext import commands  #導入指令
from core.classes import Cog_Extension #導入Cog_extension 的定義
import os
import nacl
import youtube_dl


class Music(Cog_Extension):
    
    @commands.command()
    async def play(self, ctx, url):
        guild = ctx.message.guild
        
        



def setup(bot):
    bot.add_cog(Music(bot))