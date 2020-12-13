#導入 模組
import discord  #導入Discord.py的專案
from discord.ext import commands  #導入指令
from core.classes import Cog_Extension #導入Cog_extension 的定義
from core.loggee import Loggee
import requests
import random #導入random的模組
import json  #導入json的檔案形式
import datetime #導入 時間 的模組
import os

#讀取setting.json檔案
with open('setting.json','r', encoding='utf8') as jfile:
    jdata = json.load(jfile)

class Photo(Cog_Extension):

    #指令-取得使用者頭像圖片到資料夾
    @commands.command()
    async def get_user_icon(self, ctx, member: discord.Member=None):
        now = str(datetime.datetime.now())
        loc = now.rfind('.')
        nnow = now[:loc]
        Loggee(f'[{nnow}]> 『指令』〔{ctx.author}〕 輸入 [get_user_icon]')
        await ctx.message.delete()
        if not member:
            member = ctx.message.author
        with open(F'{nnow}.jpg', 'wb') as f:
            f.write(requests.get(member.avatar_url).content)

    #指令-MC_img 隨機傳送 Minecraft 圖片
    @commands.command()
    async def MC(self, ctx):
        now = str(datetime.datetime.now())
        loc = now.rfind('.')
        nnow = now[:loc]
        Loggee(F'[{nnow}]> 『指令』 {ctx.author} 打了 [MC_img 隨機傳送 Minecraft 圖片] 指令')
        await ctx.message.delete()
        random_pic = random.choice(jdata['MC_img'])
        MC_img = discord.File(random_pic)
        await ctx.send(file= MC_img)

    #指令-MC_img 隨機傳送網路上的 Minecraft 圖片
    @commands.command()
    async def url_img(self, ctx):
        now = str(datetime.datetime.now())
        loc = now.rfind('.')
        nnow = now[:loc]
        Loggee(F'[{nnow}]> 『指令』 {ctx.author} 打了 [url_img 隨機傳送網路上的 Minecraft 圖片] 指令')
        await ctx.message.delete()
        random_pic = random.choice(jdata['url_img'])
        await ctx.send(random_pic)

    #指令-MC_img 隨機傳送 Minecraft 圖片
    @commands.command()
    async def G(self, ctx, filename):
        now = str(datetime.datetime.now())
        loc = now.rfind('.')
        nnow = now[:loc]
        Loggee(F'[{nnow}]> 『指令』 {ctx.author} 打了 [say_img 傳送圖片] 指令')
        await ctx.message.delete()
        ffile = '.\\G\\' + filename + '.png'
        img = discord.File(ffile)
        await ctx.send(file= img)

def setup(bot):
    bot.add_cog(Photo(bot))