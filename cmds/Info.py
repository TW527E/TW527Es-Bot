#導入 模組
import discord  #導入Discord.py的專案
from discord.ext import commands  #導入指令
from core.classes import Cog_Extension #導入Cog_extension 的定義
import json

#讀取setting.json檔案
with open('setting.json','r', encoding='utf8') as jfile:
    jdata = json.load(jfile)

class Info(Cog_Extension):

    #指令 - guild - 伺服器相關信息
    @commands.command()
    async def guild(self, ctx):
        print(f'【指令】〔{ctx.author}〕 輸入 [guild]')
        await ctx.message.delete()
        guild = ctx.message.guild
        guild_info = discord.Embed(title=F"{guild.name}", description="[點此到達伺服器頭像連結](%s)" % guild.icon_url, color=0xd08a2b)
        guild_info.set_thumbnail(url=F"{guild.icon_url}")
        guild_info.add_field(name="伺服器名稱", value=F"{guild.name}", inline=True)
        guild_info.add_field(name="伺服器擁有者", value=F"{guild.owner}", inline=False)
        guild_info.add_field(name="伺服器設定地區", value=F"{guild.region}", inline=True)
        guild_info.add_field(name="伺服器創建日期", value=F"{guild.created_at}", inline=False)
        guild_info.add_field(name="伺服器ID", value=F"{guild.id}", inline=True)
        guild_info.add_field(name="伺服器目前成員數量", value=F"{guild.member_count}", inline=False)
        guild_info.set_footer(text=F"此指令由 {ctx.author} 輸入 • ", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=guild_info)

    #指令 -info - 使用者相關信息
    @commands.command()
    async def info(self, ctx, member: discord.Member=None):
        print(f'【指令】〔{ctx.author}〕 輸入 [info]')
        author = ctx.message.author
        await ctx.message.delete()
        if not member:
            member = ctx.message.author
        info = discord.Embed(title=F"{member}", description="[點此到達頭像連結](%s)" % member.avatar_url, color=0xd08a2b)
        info.set_thumbnail(url=F"{member.avatar_url}")
        info.add_field(name="使用者名稱", value=F"{member.name}", inline=True)
        if str(member.status) == 'online':
            info.add_field(name="目前狀態", value=F"線上", inline=False)
        elif str(member.status) == 'offline':
            info.add_field(name="目前狀態", value=F"離線", inline=False)
        elif str(member.status) == 'idle':
            info.add_field(name="目前狀態", value=F"閒置", inline=False)
        elif str(member.status) == 'dnd':
            info.add_field(name="目前狀態", value=F"請勿打擾", inline=False)
        else:
            info.add_field(name="目前狀態", value=F"無法得知", inline=False)
        if member.activity == None:
            info.add_field(name="目前狀態消息", value="無法取得 或 沒有", inline=True)
        else:
            info.add_field(name="目前狀態消息", value=F"{member.activity}", inline=True)
        time = str(member.created_at)
        loc = time.rfind('.')
        ttime = time[:loc]
        info.add_field(name="此帳號創建日期", value=F"{ttime}", inline=False)
        join = str(member.joined_at)
        loc = join.rfind('.')
        jjoin = join[:loc]
        info.add_field(name="此帳號加入此群日期", value=F"{jjoin}", inline=True)
        roles = member.roles
        info.add_field(name="在此群擁有的所有身分組", value=F",".join([role.mention for role in roles]), inline=False)
        if member.bot is True:
            info.add_field(name="使用者是否為機器人", value="是機器人", inline=True)
        else:
            info.add_field(name="使用者是否為機器人", value="不是機器人", inline=True)
        info.add_field(name="使用者ID", value=F"{member.id}", inline=False)
        info.set_footer(text=F"此指令由 {author} 輸入 • ", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=info)



def setup(bot):
    bot.add_cog(Info(bot))

