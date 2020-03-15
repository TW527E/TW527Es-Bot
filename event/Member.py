#導入 模組
import discord  #導入Discord.py的專案
from discord.ext import commands  #導入指令
from core.classes import Cog_Extension #導入Cog_extension 的定義
import random #導入random的模組
import json  #導入json的檔案形式

#讀取setting.json檔案
with open('setting.json','r', encoding='utf8') as jfile:
    jdata = json.load(jfile)

class member(Cog_Extension):
        
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

def setup(bot):
    bot.add_cog(member(bot))