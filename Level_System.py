#導入 模組
import discord  #導入Discord.py的專案
from discord.ext import commands  #導入指令
from core.classes import Cog_Extension #導入Cog_extension 的定義
from core.loggee import Loggee
import json
import datetime
import asyncio

class Level_System(Cog_Extension):
    def __init__(self, bot):
        self.bot = bot
        self.bot.loop.create_task(self.save_users())
        #讀取Level_System.json檔案
        with open('Level_System.json', 'r', encoding='utf8') as f:
            self.users = json.load(f)
        
    async def save_users(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            #更改Level_System.json檔案
            with open('Level_System.json', 'w', encoding='utf8') as f:
                json.dump(self.users, f, indent=4)
            await asyncio.sleep(5)
            
    def level_up(self, author_id):
        cur_xp = self.users[author_id]['exp']
        cur_level = self.users[author_id]['level']

        if cur_xp >= round((4 * (cur_level * 6)) / 2):
            self.users[author_id]['level'] += 1
            self.users[author_id]['exp'] = 0
            return True
        else:
            return False

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        author_id = str(message.author.id)

        if message.author.bot is False:
            if not author_id in self.users:
                self.users[author_id] = {}
                self.users[author_id]['level'] = 1  
                self.users[author_id]['exp'] = 0
                self.users[author_id]['message'] = 1
        if message.author.bot is True:
            return
        else:
            self.users[author_id]['message'] += 1
            self.users[author_id]['exp'] += 1
        
        if self.level_up(author_id):
            level = self.users[author_id]['level']
            now = str(datetime.datetime.now())
            loc = now.rfind('.')
            nnow = now[:loc]
            Loggee(F'[{nnow}]> 『等級系統』"{message.author}" 升等了 目前等級為 "{level}"')
            await message.channel.send(F'『等級系統』**{message.author}** 你升級了**一等** 你目前等級為**{level}**')
        
    #指令-level
    @commands.command()
    async def level(self, ctx, member: discord.Member = None):
        member = ctx.author if not member else member
        member_id = str(member.id)
        llevel = self.users[member_id]['level']
        mexp =  round((4 * (llevel * 6)) / 2) - self.users[member_id]["exp"]

        now = str(datetime.datetime.now())
        loc = now.rfind('.')
        nnow = now[:loc]
        Loggee(F'[{nnow}]> 『等級系統』"{ctx.author}" 輸入了 [Level 等級顯示]')

        if not member_id in self.users:
            await ctx.send(F'『等級系統』**{ctx.author.memtion}** 你認為你在等級系統裡面的地位是人嗎?')
        else:
            embed=discord.Embed(title=F"『等級系統』 - {member.name}", description="目前在等級系統的秘密消息↓", color=0x28d252)
            embed.set_thumbnail(url=F"{member.avatar_url}")
            embed.add_field(name="目前等級", value=F"{self.users[member_id]['level']}", inline=False)
            embed.add_field(name="經驗值", value=F"還差 {mexp} 個經驗 才能升級", inline=False)
            embed.add_field(name="打了多少次訊息", value=F"{self.users[member_id]['message']}", inline=False)
            embed.set_footer(text=F"此指令由 {member.name} 輸入 • {nnow} 輸入", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Level_System(bot))