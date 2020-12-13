#導入 模組
import discord  #導入Discord.py的專案
from discord.ext import commands  #導入指令
from core.classes import Cog_Extension #導入Cog_extension 的定義
from core.loggee import Loggee
#import utils
#from discord.utils import get

class Server(Cog_Extension):

    #指令 - set_server_name - 設定伺服器名稱
    @commands.command(pass_context=True)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def set_server_name(self, ctx, *,name):
        Loggee(f'『指令-更改伺服器名稱』 {ctx.author.name} 在 {ctx.guild.name} 修改伺服器名稱為:[{name}]')
        await ctx.message.delete()
        guild_name = ctx.message.guild.name
        guild = ctx.message.guild
        await ctx.guild.edit(name=name)
        embed = discord.Embed(title=F"『指令-更改伺服器名稱』", description="[點此到達伺服器頭像連結](%s)" % guild.icon_url, color=0xd08a2b)
        embed.set_thumbnail(url=F"{guild.icon_url}")
        embed.add_field(name="更改前的伺服器名稱", value=F"{guild_name}", inline=True)
        embed.add_field(name="更改後的伺服器名稱", value=F"{name}", inline=False)
        embed.set_footer(text=F"此指令由 {ctx.author} 輸入 • ", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    #指令 - add_role
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def add_role(self, ctx, member: discord.Member=None, *, role: discord.Role):
        Loggee(f'『增加使用者身分組』 {ctx.author.name} 在 {ctx.guild.name} 建立了 {role} 身分組')
        embed = discord.Embed(title=F"『更改使用者身分組』", description="增加使用者身分組", color=0xd08a2b)
        embed.set_thumbnail(url=F"{member.avatar_url}")
        embed.add_field(name="使用者", value=F"{member}", inline=True)
        embed.add_field(name="身分組", value=F"{role}", inline=False)
        embed.set_footer(text=F"此指令由 {ctx.author} 輸入 • ", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
        await member.add_roles(role)

    #指令 - remove_role
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def remove_role(self, ctx, member: discord.Member=None, *, role: discord.Role):
        Loggee(f'『刪除使用者身分組』 {ctx.author.name} 在 {ctx.guild.name} 刪除了 {role} 身分組')
        embed = discord.Embed(title=F"『更改使用者身分組』", description="刪除使用者身分組", color=0xd08a2b)
        embed.set_thumbnail(url=F"{member.avatar_url}")
        embed.add_field(name="使用者", value=F"{member}", inline=True)
        embed.add_field(name="身分組", value=F"{role}", inline=False)
        embed.set_footer(text=F"此指令由 {ctx.author} 輸入 • ", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
        await member.remove_roles(role)

    #指令-
    @commands.command()
    async def create_role(self, ctx, role):
        await ctx.guild.create_role(role, reason=F'{ctx.author.name} 輸入指令創建此身份組')

    #指令 - 
    @commands.command() 
    async def send_guild(self, ctx, *, msg):
        counter = 0
        guild = ctx.message.guild
        #output = ' '
        author = ctx.message.author
        """for word in msg:
            output += word
            output += ' '"""
        for member in self.bot.get_all_members():
            try:
                embed = discord.Embed(title="", color=0xd08a2b)
                embed.add_field(name="**From server:**", value=guild.name)
                embed.add_field(name = "**From Mod/Admin:**", value=author.name)
                embed.add_field(name="**Message:**", value=msg)
            #   await ctx.send(embed=embed)
                
                await member.send(embed=embed)
            except (discord.HTTPException, discord.Forbidden,AttributeError):
                if counter == 1:
                    return
                counter = 1
                continue

    @commands.command()
    async def roles(self, ctx):
        Loggee(f'『群內所有身分組』 {ctx.author.name} 在 {ctx.guild.name} 輸入了 roles 顯示所有身分組')
        embed = discord.Embed(title=F"『群內所有身分組』", description="群內所有身分組", color=0xd08a2b)
        embed.set_thumbnail(url=F"{ctx.guild.icon_url}")
        embed.add_field(name="群組", value=F"{ctx.guild.name}", inline=True)
        embed.add_field(name="身分組", value=", ".join([str(r.mention) for r in ctx.guild.roles]), inline=False)
        embed.set_footer(text=F"此指令由 {ctx.author} 輸入 • ", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Server(bot))