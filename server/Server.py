#導入 模組
import discord  #導入Discord.py的專案
from discord.ext import commands  #導入指令
from core.classes import Cog_Extension #導入Cog_extension 的定義

class Server(Cog_Extension):

    #指令 - set_server_name - 設定伺服器名稱
    @commands.command(pass_context=True)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def set_server_name(self, ctx, *,name):
        await ctx.message.delete()
        guild_name = ctx.message.guild.name
        guild = ctx.message.guild
        await ctx.guild.edit(name=name)
        embed = discord.Embed(title=F"『更改伺服器名稱』", description="[點此到達伺服器頭像連結](%s)" % guild.icon_url, color=0xd08a2b)
        embed.set_thumbnail(url=F"{guild.icon_url}")
        embed.add_field(name="更改前的伺服器名稱", value=F"{guild_name}", inline=True)
        embed.add_field(name="更改後的伺服器名稱", value=F"{name}", inline=False)
        embed.set_footer(text=F"此指令由 {ctx.author} 輸入 • ", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Server(bot))