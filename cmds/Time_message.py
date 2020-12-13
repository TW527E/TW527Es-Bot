#導入 模組
import discord  #導入Discord.py的專案
from discord.ext import commands  #導入指令
from core.classes import Cog_Extension #導入Cog_extension 的定義
import json, asyncio, datetime #導入 json 異步協程 時間 的模組

class Time_message(Cog_Extension):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.counter = 0
    
        async def status():
            await self.bot.wait_until_ready()
            while not self.bot.is_closed():
                if discord.Streaming:
                    await self.bot.change_presence(activity=discord.Activity(name="|help 獲取指令提示幫助", type=discord.ActivityType.watching))
                    await asyncio.sleep(3)
                if discord.Streaming:
                    await self.bot.change_presence(activity=discord.Activity(name="我是最帥的苦力怕", type=discord.ActivityType.watching))
                    await asyncio.sleep(3)
                if discord.Streaming:
                    await self.bot.change_presence(activity=discord.Activity(name="作者:誠誠 - TW527E#8668", type=discord.ActivityType.watching))
                    await asyncio.sleep(3)

        self.bg_time_message = self.bot.loop.create_task(status())
    

        async def timsg():
            await self.bot.wait_until_ready()
            self.channel = self.bot.get_channel()
            while not self.bot.is_closed():

                now_time = datetime.datetime.now().strftime('%H%M')
                #讀取setting.json檔案
                with open('setting.json','r', encoding='utf8') as jfile:
                    jdata = json.load(jfile)
                if now_time == jdata['time'] and self.counter == 0:
                    await self.channel.send('test')
                    self.counter = 1
                    await asyncio.sleep(1)
                else:
                    await asyncio.sleep(1)
                    pass

        self.bg_time_message = self.bot.loop.create_task(timsg())

    #指令-set_auto_msg_time  設定發送公告時間
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def set_auto_time(self, ctx, mn, hr: int, min: int):
        self.counter = 0
        await ctx.message.delete()
        
        if mn == '早上':
            mn = 'morning'
        elif mn == '早':
            mn = 'morning'
        elif mn == 'morning':
            mn = 'morning'
        elif mn == 'm':
            mn = 'morning'
        elif mn == '晚上':
            mn = 'night'
        elif mn == '晚':
            mn = 'night'
        elif mn == 'night':
            mn = 'night'
        elif mn == 'n':
            mn = 'night'
        
        if hr >> 12  and hr <= 24:
            hr = hr - 12
        elif hr >> 24:
            await ctx.send('『公告設定』你有病是吧? (錯誤:小時過大)')
            print('『公告設定』錯誤:小時過大')
        elif hr << 0:
            await ctx.send('『公告設定』你有病是吧? (錯誤:小時過小)')
            print('『公告設定』錯誤:小時過小')

        if min >= 61 or min << 0:
            if min >= 61:
                await ctx.send('『公告設定』你有病是吧? (錯誤:分鐘過大)')
                print('『公告設定』錯誤:分鐘過大')
            elif min << 0:
                await ctx.send('『公告設定』你有病是吧? (錯誤:分鐘過小)')
                print('『公告設定』錯誤:分鐘過小')

        with open('setting.json', mode='r', encoding='utf8') as jfile:
            jdata = json.load(jfile)
        jdata['time'] = time
        with open('setting.json', mode='w', encoding='utf8') as jfile:
            json.dump(jdata, jfile, indent=4)
        await ctx.send(f'『公告設定』自動公告發送時間 已設定為 [{time}]')

    #指令-set_auto_ch  設定發送公告頻道
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def set_auto_ch(self, ctx, ch:int):
        await ctx.message.delete()
        self.channel = self.bot.get_channel(ch)
        await ctx.send(f'『公告設定』自動公告頻道 已設定為 [{self.channel.mention}] 頻道')
    
    #指令-
    @commands.command()
    async def abc(self, ctx):
        now_time = datetime.datetime.now().strftime('%H%M')
        print(now_time)

def setup(bot):
    bot.add_cog(Time_message(bot))