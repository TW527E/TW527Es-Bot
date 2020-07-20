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
            embed=discord.Embed(title=F"『{member.mention}』 加入了伺服器", color=0xd08a2b)
            embed.set_thumbnail(url="{}".format(member.avatar_url))
            await channel.send(embed=embed)
            '''await channel.send(F'>> {member.mention} << 加入了伺服器')'''
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

    #伺服器-Reaction Role 新增反應貼圖獲得身分組
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        print(F'『{payload.member}』加入反應 已獲得Steve')
        if payload.message_id == 667987897588121610:
            if str(payload.emoji) == '<:Taiwan:734310979948773407>':
                guild = self.bot.get_guild(payload.guild_id)
                role = guild.get_role(470078983325745152)
                await payload.member.add_roles(role)
                await payload.member.send('''恭喜你撐過了這艱難的10分鐘:partying_face: 

                你獲得了 『Steve』 身分組 

                如果你是Minecraft玩家 記得在TaiwanMC的Minecraft伺服器裡面
                連結你的Discord帳號
                只要打 /discord link
                就可以知道之後要怎麼辦了''')
            else:
                pass
        else:
            pass

    #伺服器-Reaction Role 移除反應貼圖移除身分組
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if payload.message_id == 667987897588121610:
            if str(payload.emoji) == '<:Taiwan:734310979948773407>':
                guild = self.bot.get_guild(payload.guild_id)
                user = guild.get_member(payload.user_id)
                print(F'『{user}』移除反應 刪除了Steve')
                role = guild.get_role(470078983325745152)
                await user.remove_roles(role)
                await user.send('''等等 你怎麼按到移除的!!
                你該不會退出過伺服器了吧
                不乖喔''')
            else:
                pass
        else:
            pass

def setup(bot):
    bot.add_cog(member(bot))