#導入 模組
import discord  #導入Discord.py的專案
from discord.ext import commands  #導入指令
from core.classes import Cog_Extension #導入Cog_extension 的定義

class Status(Cog_Extension):

    #指令-shutdown 下線
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def shutdown(self, ctx):
        print(F'《指令》〔{ctx.author}〕 輸入 [shutdown - 機器人關機] 指令')
        await ctx.message.delete()
        await ctx.send('【狀態】掰掰 我已關機')
        await self.bot.change_presence(status=discord.Status.offline)

    #指令-online 上線
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def online(self, ctx):
        print(F'《指令》〔{ctx.author}〕 輸入 [online - 機器人上線] 指令')
        await ctx.message.delete()
        await ctx.send('【狀態】你好 我已經啟動!')
        await self.bot.change_presence(status=discord.Status.online, activity=discord.Game('|cmds 獲取指令提示幫助'))

    #指令-idle 
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def idle(self, ctx):
        print(F'《指令》〔{ctx.author}〕 輸入 [idle - 機器人閒置] 指令')
        await ctx.message.delete()
        await ctx.send('【狀態】我太懶了 不想做事!')
        await self.bot.change_presence(status=discord.Status.idle, activity=discord.Game('ヾ(≧ ▽ ≦)ゝ'))

    #指令-dnd
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def dnd(self, ctx):
        print(F'《指令》〔{ctx.author}〕 輸入 [dnd - 機器人請勿打擾] 指令')
        await ctx.message.delete()
        await ctx.send('【狀態】機器人測試中 請勿打擾')
        await self.bot.change_presence(status=discord.Status.dnd, activity=discord.Game('機器人測試中 請勿打擾'))

def setup(bot):
    bot.add_cog(Status(bot))