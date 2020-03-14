#導入 模組
import discord  #導入Discord.py的專案
from discord.ext import commands  #導入指令
from core.classes import Cog_Extension #導入Cog_extension 的定義
import os
import nacl


class Channel(Cog_Extension):
    
    @commands.command()
    async def join(self, ctx):
        print(f'《語音頻道》〔{ctx.author}〕 輸入 [join] 使機器人加入頻道')
        channel = ctx.author.voice.channel
        await ctx.message.delete()
        await channel.connect()
        await ctx.send(f'《語音頻道》已加入到 《**{channel}**》')


    @commands.command()
    async def leave(self, ctx):
        print(f'《語音頻道》〔{ctx.author}〕 輸入 [leave] 使機器人退出頻道')
        await ctx.message.delete()
        await ctx.voice_client.disconnect()
        await ctx.send('《語音頻道》已退出 **語音頻道**')

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def add_text_ch(self, ctx, *, msg):
        guild = ctx.message.guild
        print(f'《文字頻道》創建文字頻道 在〘**{guild}**〙')
        await ctx.message.delete()
        await guild.create_text_channel(msg)
        await ctx.send(f'《文字頻道》創建文字頻道 在〘**{guild}**〙')

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def add_voice_ch(self, ctx, *, msg):
        guild = ctx.message.guild
        print(f'《語音頻道》創建語音頻道 在〘**{guild}**〙')
        await ctx.message.delete()
        await guild.create_voice_channel(msg)
        await ctx.send(f'《語音頻道》創建語音頻道 在〘**{guild}**〙')
        

def setup(bot):
    bot.add_cog(Channel(bot))