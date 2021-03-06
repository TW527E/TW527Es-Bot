#導入 模組
import discord  #導入Discord.py的專案
from discord.ext import commands  #導入指令
from core.classes import Cog_Extension #導入Cog_extension 的定義
import random #導入random的模組
import json  #導入json的檔案形式
import datetime

#讀取setting.json檔案
with open('setting.json','r', encoding='utf8') as jfile:
    jdata = json.load(jfile)

#讀取 servers/taiwanmc.json檔案
with open('servers/taiwanmc.json', 'r', encoding='utf8') as tmc:
    taiwanmc_data = json.load(tmc)

#讀取 servers/IT.json檔案
with open('servers/IT.json', 'r', encoding='utf8') as itt:
    it_data = json.load(itt)

class member(Cog_Extension):
        
    #伺服器通知-有人加入了伺服器(setting.json)
    @commands.Cog.listener()
    async def on_member_join(self, member):
        now = str(datetime.datetime.now())
        loc = now.rfind('.')
        nnow = now[:loc]
        if str(member.guild.id) == str(taiwanmc_data['guild_id']): #TaiwanMC
            print(F'[{nnow}]> 『{member}』 加入了《{member.guild.name}》伺服器')
            channel = self.bot.get_channel(int(taiwanmc_data['member_join_channel']))
            embed=discord.Embed(title=F"『{member}』 加入了伺服器", color=0xd08a2b)
            embed.set_thumbnail(url="{}".format(member.avatar_url))
            await channel.send(embed=embed)
            '''await channel.send(F'>> {member.mention} << 加入了伺服器')'''
        if str(member.guild.id) == str(it_data['guild_id']): #IT
            print(F'[{nnow}]> 『{member}』 加入了《{member.guild.name}》伺服器')
            channel = self.bot.get_channel(int(it_data['member_join_channel']))
            embed=discord.Embed(title=F"『{member}』 加入了伺服器", color=0xd08a2b)
            embed.set_thumbnail(url="{}".format(member.avatar_url))
            await channel.send(embed=embed)
            '''await channel.send(F'>> {member.mention} << 加入了伺服器')'''
        else:
            pass

    #伺服器通知-有人退出了伺服器(setting.json)
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        now = str(datetime.datetime.now())
        loc = now.rfind('.')
        nnow = now[:loc]
        if str(member.guild.id) == str(taiwanmc_data['guild_id']): #TaiwanMC
            print(F'[{nnow}]> 『{member}』 退出了"{member.guild.name}"')
            channel = self.bot.get_channel(int(jdata['member_leave_channel']))
            await channel.send(F'>> {member} << 退出了伺服器')
        if str(member.guild.id) == str(it_data['guild_id']): #IT
            print(F'[{nnow}]> 『{member}』 退出了《{member.guild.name}》伺服器')
            channel = self.bot.get_channel(int(it_data['member_leave_channel']))
            embed=discord.Embed(title=F"『{member}』 退出了伺服器", color=0xd08a2b)
            embed.set_thumbnail(url="{}".format(member.avatar_url))
            await channel.send(embed=embed)
        else:
            pass

    #伺服器-Reaction Role 新增反應貼圖獲得身分組
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        now = str(datetime.datetime.now())
        loc = now.rfind('.')
        nnow = now[:loc]
        #TaiwanMC
        if int(payload.message_id) == int(taiwanmc_data['Reaction_Msg']):
            if str(payload.emoji) == str(taiwanmc_data['Reaction_Emoji']):
                guild = self.bot.get_guild(payload.guild_id)
                role = guild.get_role(int(taiwanmc_data['Reaction_Role']))
                role2 = guild.get_role(int(taiwanmc_data['Reaction_Role2']))
                print(F'[{nnow}]> 《{guild.name}》『{payload.member}』加入反應 已獲得《{role.name}》')
                await payload.member.add_roles(role, role2)
                await payload.member.send('''恭喜你成為了『TaiwanMC』的一員:partying_face: 

                你獲得了 『Steve』 身分組 

                如果你是Minecraft玩家 記得在TaiwanMC的Minecraft伺服器裡面
                連結你的Discord帳號
                只要打 /discord link
                就可以知道之後要怎麼辦了
                
                (我是群主自製小機器人喔)''')
        #ITDT
        if int(payload.message_id) == int(it_data['Reaction_Msg']):
            if str(payload.emoji) == str(it_data['Reaction_Emoji']):
                guild = self.bot.get_guild(payload.guild_id)
                role = guild.get_role(int(it_data['Reaction_Role']))
                print(F'[{nnow}]> 『{payload.member}』加入反應 已獲得《{role.name}》')
                await payload.member.add_roles(role)
                await payload.member.send(F'《恭喜》你已獲得了 《{role.name}》')
                await payload.member.send(F'《Congratulations》you have won 《{role.name}》')
        
    #伺服器-Reaction Role 移除反應貼圖移除身分組
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        now = str(datetime.datetime.now())
        loc = now.rfind('.')
        nnow = now[:loc]
        #TaiwanMC
        if str(payload.message_id) == str(taiwanmc_data['Reaction_Msg']):
            if str(payload.emoji) == taiwanmc_data['Reaction_Emoji']:
                guild = self.bot.get_guild(payload.guild_id)
                user = guild.get_member(payload.user_id)
                print(F'[{nnow}]> 《{guild.name}》『{payload.member}』加入反應 已獲得《{role.name}》')
                role = guild.get_role(int(taiwanmc_data['Reaction_Role']))
                role2 = guild.get_role(int(taiwanmc_data['Reaction_Role2']))
                await user.remove_roles(role, role2)
                await user.send('.....')
        #ITDT
        if str(payload.message_id) == str(it_data['Reaction_Msg']):
            if str(payload.emoji) == it_data['Reaction_Emoji']:
                guild = self.bot.get_guild(payload.guild_id)
                user = guild.get_member(payload.user_id)
                print(F'[{nnow}]> 《{guild.name}》『{payload.member}』加入反應 已獲得《{role.name}》')
                role = guild.get_role(int(it_data['Reaction_Role']))
                await user.remove_roles(role)
                await user.send('.....')


def setup(bot):
    bot.add_cog(member(bot))