#導入 模組
import discord  #導入Discord.py的專案
from discord.ext import commands  #導入指令
from core.classes import Cog_Extension #導入Cog_extension 的定義

class Status(Cog_Extension):

    #指令-shutdown 下線
    @commands.command()
    @commands.is_owner()
    async def shutdown(self, ctx):
        print(F'《指令》〔{ctx.author}〕 輸入 [shutdown - 機器人關機] 指令')
        await ctx.message.delete()
        await ctx.send('【狀態】掰掰 我已關機')
        await self.bot.change_presence(status=discord.Status.offline)

    #指令-online 上線
    @commands.command()
    @commands.is_owner()
    async def online(self, ctx):
        print(F'《指令》〔{ctx.author}〕 輸入 [online - 機器人上線] 指令')
        await ctx.message.delete()
        await ctx.send('【狀態】你好 我已經啟動!')
        await self.bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name="|help 獲取指令提示幫助"))

    #指令-idle 
    @commands.command()
    @commands.is_owner()
    async def idle(self, ctx):
        print(F'《指令》〔{ctx.author}〕 輸入 [idle - 機器人閒置] 指令')
        await ctx.message.delete()
        await ctx.send('【狀態】我太懶了 不想做事!')
        await self.bot.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.watching, name="ψ(｀∇´)ψ"))

    #指令-dnd
    @commands.command()
    @commands.is_owner()
    async def dnd(self, ctx):
        print(F'《指令》〔{ctx.author}〕 輸入 [dnd - 機器人請勿打擾] 指令')
        await ctx.message.delete()
        await ctx.send('【狀態】不要打擾我( •̀ ω •́ )✧')
        await self.bot.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.watching, name="不要吵我`(*>﹏<*)′"))

    #指令-dnd
    @commands.command()
    @commands.is_owner()
    async def test(self, ctx):
        print(F'《指令》〔{ctx.author}〕 輸入 [test - 機器人測試中] 指令')
        await ctx.message.delete()
        await ctx.send('【狀態】機器人測試中 請勿打擾')
        await self.bot.change_presence(activity=discord.Streaming(name="機器人測試中", url="https://www.twitch.tv/tw527e"))

def setup(bot):
    bot.add_cog(Status(bot))