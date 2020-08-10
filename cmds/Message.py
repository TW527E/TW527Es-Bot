#導入 模組
import discord  #導入Discord.py的專案
from discord.ext import commands  #導入指令
from core.classes import Cog_Extension #導入Cog_extension 的定義
import random #導入random的模組
import json  #導入json的檔案形式
import datetime #導入 時間 的模組

#讀取setting.json檔案
with open('setting.json','r', encoding='utf8') as jfile:
    jdata = json.load(jfile)

class Message(Cog_Extension):

    #指令-MC_img 隨機傳送 Minecraft 圖片
    @commands.command()
    async def MC(self, ctx):
        print(F'【指令】 {ctx.author} 打了 [MC_img 隨機傳送 Minecraft 圖片] 指令')
        await ctx.message.delete()
        random_pic = random.choice(jdata['MC_img'])
        MC_img = discord.File(random_pic)
        await ctx.send(file= MC_img)

    #指令-MC_img 隨機傳送網路上的 Minecraft 圖片
    @commands.command()
    async def url_img(self, ctx):
        print(F'【指令】 {ctx.author} 打了 [url_img 隨機傳送網路上的 Minecraft 圖片] 指令')
        await ctx.message.delete()
        random_pic = random.choice(jdata['url_img'])
        await ctx.send(random_pic)

    #指令-say_msg 機器人訊息複誦
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def say_msg(self, ctx, *,msg):
        print(F'【指令】 {ctx.author} 打了 [say_messange 訊息復誦] 指令 讓機器人說出 [{msg}]')
        await ctx.message.delete()
        await ctx.send(msg)
    
    #指令-del_msg 機器人清理訊息
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def del_msg(self, ctx, num:int):
        print(F'【指令】 {ctx.author} 打了 [del_messange 刪除訊息] 指令')
        await ctx.message.delete()
        await ctx.channel.purge(limit=num)

    #指令 - say_dm - 傳送私聊訊息
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def say_dm(self, ctx, member: discord.Member=None, *, msg):
        print(f'【指令】〔{ctx.author}〕 輸入 [say_dm]')
        await ctx.message.delete()
        if not member:
            member = ctx.message.author
        guild = self.bot.get_guild(ctx.author.guild.id)
        member_user = guild.get_member(member.id)
        await member_user.send(msg)
        embed = discord.Embed(title=F"『私訊聊天室』", description="[點此到達指定使用者頭像連結](%s)" % member.avatar_url, color=0xd08a2b)
        embed.set_thumbnail(url=F"{member.avatar_url}")
        embed.add_field(name="指定使用者", value=F"{member.name}", inline=True)
        embed.add_field(name="指定的訊息", value=F"{msg}", inline=False)
        embed.set_footer(text=F"此指令由 {ctx.author} 輸入 • ", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
    
    #指令-now_time 現在時間
    @commands.command()
    async def now_time(self, ctx):
        print(F'【指令】 {ctx.author} 打了 [now_time 現在時間] 指令')
        await ctx.message.delete()
        now = datetime.datetime.now()
        loc = now.rfind('.')
        nnow = now[:loc]
        await ctx.send(F'現在機器人的時間是 {nnow}')

def setup(bot):
    bot.add_cog(Message(bot))