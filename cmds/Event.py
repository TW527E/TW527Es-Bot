#導入 模組
import discord  #導入Discord.py的專案
from discord.ext import commands  #導入指令
from core.classes import Cog_Extension #導入Cog_extension 的定義
import random #導入random的模組
import json  #導入json的檔案形式

#讀取setting.json檔案
with open('setting.json','r', encoding='utf8') as jfile:
    jdata = json.load(jfile)

class Event(Cog_Extension):
        
    #伺服器通知-有人加入了伺服器(setting.json)
    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.guild.id == 447628147286999042:
            print(F'> 〔{member}〕 加入了伺服器')
            channel = self.bot.get_channel(int(jdata['member_join_channel']))
            await channel.send(F'>> {member.mention} << 加入了伺服器')
        else:
            pass

    #伺服器通知-有人退出了伺服器(setting.json)
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if member.guild.id == 447628147286999042:
            print(F'> 〔{member}〕 退出了伺服器')
            channel = self.bot.get_channel(int(jdata['member_leave_channel']))
            await channel.send(F'>> {member} << 退出了伺服器')
        else:
            pass

    #訊息對話
    @commands.Cog.listener()
    async def on_message(self, msg):
        #早安
        keyword = ['早安', '早', '早安!', ' 早!', '大家早安', '大家早安!', '大家早安阿', '大家早安啊', '大家早安ㄚ', '大家早安阿!', '大家早安啊!', '大家早安ㄚ!']
        if msg.content == '早安' and msg.author != self.bot.user:
            await msg.channel.send('早安! 祝你有個美好的一天!')
            print('有人打入了 [早安] 的關鍵字 因此 觸發了[早安! 祝你有個美好的一天!]')
        #晚安        
        keyword = ['晚安', '晚安!', '我先睡了', '我先睡了!']
        if msg.content in keyword and msg.author != self.bot.user:
            await msg.channel.send('晚安! 祝你有個好夢!')
            print('有人打入了 [晚安] 的關鍵字 因此 觸發了[晚安! 祝你有個好夢!]')
        #警告機制
        keyword = ['Fuck', 'FUck', 'FUCk', 'FUCK', 'fUCK', 'fuCK', 'fucK', 'fuck', 'fUck', 'fUCk', 'fUCK', 'FUck', 'FUCk', 'FuCk', 'FUcK', 'FuCk', '幹你娘', '操你媽', '幹', '看屁阿鄉巴佬']
        if msg.content in keyword and msg.author !=self.bot.user:
            await msg.delete()
            await msg.channel.send(F'【警告】請勿輸入相關不雅詞語!  懲罰: 警告x1')
            print('有人打入了 [不雅的詞語] 因此 觸發了[警告機制]')

def setup(bot):
    bot.add_cog(Event(bot))