#導入 模組
import discord  #導入Discord.py的專案
from discord.ext import commands  #導入指令
from core.classes import Cog_Extension #導入Cog_extension 的定義
import json, asyncio, datetime #導入 json 異步協程 時間 的模組

class Time_message(Cog_Extension):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
        async def interval():
            await self.bot.wait_until_ready()
            self.channel = self.bot.get_channel(668698688578650113)
            while not self.bot.is_closed():
                print('【公告-狀態】[300秒] 訊息:[嗨 我正在運行! 可以使用我喔!]')
                await self.channel.send('嗨 我正在運行! 可以使用我喔!')
                await asyncio.sleep(600) #單位 = 秒

        self.bg_time_message = self.bot.loop.create_task(interval())
    
    #指令-set_auto_ch  設定發送公告頻道
    @commands.command()
    async def set_auto_ch(self, ctx, ch: int):
        await ctx.message.delete()
        self.channel = self.bot.get_channel(ch)
        print(F'有人打了 [set_auto_ch {self.channel} 設定公告發送頻道] 指令')
        await ctx.send(F'【公告】公告頻道設置 已設定為 [{self.channel.mention}] 頻道')

    #指令-set_auto_msg_time  設定發送公告時間
    @commands.command()
    async def set_auto_time(self, ctx, time):
        #讀取setting.json檔案
        with open('setting.json','r', encoding='utf8') as jfile:
            jdata = json.load(jfile)
        jdata['auto_msg_time'] = time
        #寫入setting.json檔案
        with open('setting.json','w', encoding='utf8') as jfile:
            json.dump(jdata, jfile, indent=4)

        
    

def setup(bot):
    bot.add_cog(Time_message(bot))