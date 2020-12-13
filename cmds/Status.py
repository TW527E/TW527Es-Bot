#導入 模組
import discord  #導入Discord.py的專案
from discord.ext import commands  #導入指令
from core.classes import Cog_Extension #導入Cog_extension 的定義
from core.loggee import Loggee
import datetime

class Status(Cog_Extension):
    
    #指令-shutdown 下線
    @commands.command()
    @commands.is_owner()
    async def shutdown(self, ctx):
        now = str(datetime.datetime.now())
        loc = now.rfind('.')
        nnow = now[:loc]
        Loggee(f'『指令』〔{ctx.author}〕 輸入 [shutdown - 機器人關機] 指令')
        await ctx.message.delete()
        await ctx.send('【狀態】掰掰 我已關機')
        await self.bot.change_presence(status=discord.Status.offline)

    #指令-online 上線
    @commands.command()
    @commands.is_owner()
    async def online(self, ctx):
        now = str(datetime.datetime.now())
        loc = now.rfind('.')
        nnow = now[:loc]
        Loggee(f'『指令』〔{ctx.author}〕 輸入 [online - 機器人上線] 指令')
        await ctx.message.delete()
        await ctx.send('【狀態】你好 我已經啟動!')
        await self.bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name="我現在不知道要幹嘛...."))

    #指令-idle 
    @commands.command()
    @commands.is_owner()
    async def idle(self, ctx):  
        now = str(datetime.datetime.now())
        loc = now.rfind('.')
        nnow = now[:loc]
        Loggee(f'『指令』〔{ctx.author}〕 輸入 [idle - 機器人閒置] 指令')
        await ctx.message.delete()
        await ctx.send('【狀態】我太懶了 不想做事!')
        await self.bot.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.watching, name="ψ(｀∇´)ψ"))

    #指令-dnd
    @commands.command()
    @commands.is_owner()
    async def dnd(self, ctx):
        now = str(datetime.datetime.now())
        loc = now.rfind('.')
        nnow = now[:loc]
        Loggee(f'『指令』〔{ctx.author}〕 輸入 [dnd - 機器人請勿打擾] 指令')
        await ctx.message.delete()
        await ctx.send('【狀態】不要打擾我( •̀ ω •́ )✧')
        await self.bot.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.watching, name="不要吵我`(*>﹏<*)′"))

    #指令-inv
    @commands.command()
    @commands.is_owner()
    async def inv(self, ctx):
        now = str(datetime.datetime.now())
        loc = now.rfind('.')
        nnow = now[:loc]
        Loggee(f'『指令-機器人隱形』"{ctx.author}" 輸入 [invisible - ] 指令')
        await ctx.message.delete()
        await self.bot.change_presence(status=discord.Status.invisible)

    #指令-test
    @commands.command()
    @commands.is_owner()
    async def test(self, ctx):
        now = str(datetime.datetime.now())
        loc = now.rfind('.')
        nnow = now[:loc]
        Loggee(f'『指令-機器人測試中』"{ctx.author}" 輸入 [test - 機器人測試中] 指令')
        await ctx.message.delete()
        await ctx.send('【狀態】機器人測試中 請勿打擾')
        await self.bot.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.watching, name="機器人測試中"))
        
    #指令-status
    @commands.command()
    @commands.is_owner()
    async def status(self, ctx, sstatus, *, nname = None):
        now = str(datetime.datetime.now())
        loc = now.rfind('.')
        nnow = now[:loc]
        Loggee(f'『指令』"{ctx.author}" 輸入 [status {sstatus} {nname}]')
        await ctx.message.delete()
        if nname == None:
            nname = 'ヾ(•ω•`)o'
        if sstatus == '線上':
            await self.bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name=F"{nname}"))
            sstatus = '線上'
        elif sstatus == 'idle':
            await self.bot.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.watching, name=F"{nname}"))
            sstatus = '閒置'
        elif sstatus == 'dnd':
            await self.bot.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.watching, name=F"{nname}"))
            sstatus = '請勿打擾'
        else:
            await ctx.send('『ERROR』你可能 打錯了甚麼吧')
            return
        await ctx.send(F'【狀態】目前狀態:{sstatus} 目前狀態消息:{nname}')

def setup(bot):
    bot.add_cog(Status(bot))