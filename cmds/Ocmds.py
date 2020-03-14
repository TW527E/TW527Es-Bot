#導入 模組
import discord  #導入Discord.py的專案
from discord.ext import commands  #導入指令
from core.classes import Cog_Extension #導入Cog_extension 的定義

class Ocmds(Cog_Extension):
    
    @commands.group()
    async def like(self, ctx):
        await ctx.send('''Do you like
        1.eevee
        2.minecraft
        3.FUCK''')

    @like.command()
    async def eevee(self, ctx):
        await ctx.send("幹你娘")
        
    @like.command()
    async def minecraft(self, ctx):
        await ctx.send("真的?? 我也很喜歡!")
    
    @like.command()
    async def FUCK(self, ctx):
        await ctx.send("看來你很喜歡FUCK!  FUCKFUCKFUCKFUCKFUCKFUCKFUCKFUCKFUCKFUCKFUCKFUCKFUCKFUCKFUCKFUCK")

def setup(bot):
    bot.add_cog(Ocmds(bot))