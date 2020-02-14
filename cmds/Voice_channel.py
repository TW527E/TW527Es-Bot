#導入 模組
import discord  #導入Discord.py的專案
from discord.ext import commands  #導入指令
from core.classes import Cog_Extension #導入Cog_extension 的定義
import os
import nacl


class Voice_channel(Cog_Extension):
    
    @commands.command()
    async def join(self, ctx):
        print(f'《語音頻道》{ctx.author} 打入了 [join] 讓機器人加入頻道')
        channel = ctx.author.voice.channel
        await ctx.message.delete()
        await channel.connect()
        await ctx.send(f'《語音頻道》已加入到 《**{channel}**》')


    @commands.command()
    async def leave(self, ctx):
        print(f'《語音頻道》{ctx.author} 打入了 [leave] 讓機器人加入 [頻道')
        await ctx.message.delete()
        await channel.disconnect()
        await ctx.send('《語音頻道》已退出 語音頻道*')

def setup(bot):
    bot.add_cog(Voice_channel(bot))