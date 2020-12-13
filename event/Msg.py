#導入 模組
import discord  #導入Discord.py的專案
from discord.ext import commands  #導入指令
from core.loggee import Loggee
from core.classes import Cog_Extension #導入Cog_extension 的定義
import random #導入random的模組
import json  #導入json的檔案形式
import datetime
import re
#讀取setting.json檔案
with open('setting.json','r', encoding='utf8') as jfile:
    jdata = json.load(jfile)

class Msg(Cog_Extension):
        
    #訊息對話
    @commands.Cog.listener()
    async def on_message(self, msg):
        #早安
        keyword = ['早安', '早', '早安!', ' 早!', '大家早安', '大家早安!', '大家早安阿', '大家早安啊', '大家早安ㄚ', '大家早安阿!', '大家早安啊!', '大家早安ㄚ!']
        if msg.content == keyword and msg.author != self.bot.user:
            await msg.channel.send('早安! 祝你有個美好的一天!')
            Loggee(F'『訊息觸發』[{msg.author}] 輸入了 [{msg.content}] 因此 觸發了 [早安! 祝你有個美好的一天!]')
        #午安
        keyword = ['午安', '午安!', '睡午覺', '睡午覺!']
        if msg.content in keyword and msg.author != self.bot.user:
            await msg.channel.send('午安!')
            Loggee(F'『訊息觸發』[{msg.author}] 輸入了 [{msg.content}] 的關鍵字 因此 觸發了[午安!]')
        #晚安        
        keyword = ['晚安', '晚安!', '我先睡了', '我先睡了!']
        if msg.content in keyword and msg.author != self.bot.user:
            await msg.channel.send('晚安! 祝你有個好夢!')
            Loggee(F'『訊息觸發』[{msg.author}] 輸入了 [{msg.content}] 因此 觸發了[晚安! 祝你有個好夢!]')
        #?
        keyword = ['?', 'wtf', 'Wtf', 'WTF', 'wtf!', 'Wtf!', 'WTF!', 'wtf?', 'Wtf?', 'WTF?']
        if msg.content in keyword and msg.author != self.bot.user:
            await msg.channel.send('https://tenor.com/view/nick-young-question-mark-huh-what-confused-gif-4995479')
            Loggee(F'『訊息觸發』[{msg.author}] 輸入了 [{msg.content}] 因此 觸發了[https://tenor.com/view/nick-young-question-mark-huh-what-confused-gif-4995479]')
        #嗨起來
        keyword = ['嗨起來', '嗨起來!']
        if msg.content in keyword and msg.author != self.bot.user:
            await msg.channel.send('有人提到嗨起來嗎!?')
            await msg.channel.send('https://tenor.com/view/high-gif-5005257')
            Loggee(F'『訊息觸發』[{msg.author}] 輸入了 [{msg.content}] 因此 觸發了[有人提到嗨起來嗎!? https://tenor.com/view/high-gif-5005257]')
        #警告機制
        keyword = ['Fuck', 'FUck', 'FUCk', 'FUCK', 'fUCK', 'fuCK', 'fucK', 'fuck', 'fUck', 'fUCk', 'fUCK', 'FUck', 'FUCk', 'FuCk', 'FUcK', 'FuCk', '幹你娘', '操你媽', '幹', '看屁阿鄉巴佬']
        if msg.content in keyword and msg.author !=self.bot.user:
            if msg.guild.id == 447628147286999042:
                await msg.delete()
                self.channel = self.bot.get_channel(669130768072704002)
                is_msg(keyword, F'{msg.content}')
                await self.channel.send(F'『{msg.author.mention}』請勿輸入相關不雅詞語!  懲罰: 警告x1')
                Loggee(F'『訊息觸發』[{msg.author}] 輸入了 [{msg.content}] 因此 觸發了[警告機制]')

    @commands.Cog.listener()
    async def on_raw_message_delete(self, payload):
        counter = 1
        gguild = self.bot.get_guild(payload.guild_id)
        async for auditlog in gguild.audit_logs(action=discord.AuditLogAction.message_delete):
            if counter == 1:
                now = str(datetime.datetime.now())
                loc = now.rfind('.')
                nnow = now[:loc]
                ch = self.bot.get_channel(774791627490197524)
                msgch = self.bot.get_channel(auditlog.message.id)
                embed = discord.Embed(title=F"『訊息刪除紀錄』", description="[點此到達指定使用者頭像連結](%s)" % auditlog.user.avatar_url, color=0xd08a2b)
                embed.set_thumbnail(url=F"{auditlog.user.avatar_url}")
                embed.add_field(name="使用者", value=F"{auditlog.user.name}", inline=True)
                embed.add_field(name="頻道", value=F"{msgch.name}", inline=True)
                embed.add_field(name="使用者", value=F"{auditlog.user.name}", inline=False)
                embed.set_footer(text=F"此訊息刪除時間 [{nnow}] ", icon_url=auditlog.user.avatar_url)
                await ch.send(embed=embed)
                counter += 1

            #await channel.send(F'使用者『{msg.author}』 刪除了 〔{msg.content}〕')

def setup(bot):
    bot.add_cog(Msg(bot))