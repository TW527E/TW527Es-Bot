#導入 模組
import discord  #導入Discord.py的專案
from discord.ext import commands  #導入指令
from core.classes import Cog_Extension #導入Cog_extension 的定義

class Main(Cog_Extension):

    #指令-cmd 控制台指令
    @commands.command()
    @commands.is_owner()
    async def cmd(self, ctx, *, test):
        import os,traceback
        print(os.system(f"{test}"))
        await ctx.send('《指令》已執行')

    #指令-Ping 延遲
    @commands.command()
    async def ping(self, ctx):
        print(F'《指令》〔{ctx.author}〕 輸入 [ping 機器人延遲] 指令')
        await ctx.message.delete()
        await ctx.send(F'{round(self.bot.latency*1000)} 毫秒(ms)')

    #指令-kick 踢人
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def kick(self, ctx, member : discord.Member, *, reason=None):
        await ctx.message.delete()
        await member.kick(reason=reason)
        print(F'《指令》〔{ctx.author}〕 輸入 [kick {member}] 指令')
        await ctx.send(F'使用者 **{member}** 已被踢出')

    #指令-Ban 封鎖
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def ban(self, ctx, member : discord.Member, *, reason=None):
        await ctx.message.delete()
        await member.ban(reason=reason)
        print(F'《指令》〔{ctx.author}〕 輸入 [ban {member.name}] 指令')
        await ctx.send(F'使用者 >>**{member.name}**<< 已被封鎖')

    #指令-unBan 解除封鎖
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def unban(self, ctx, *, member):
        await ctx.message.delete()
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                print(F'《指令》〔{ctx.author}〕 輸入 [unban {user}] 指令')
                await ctx.send(F'使用者 >>**{user}**<< 已經解除封鎖')
                return

    #指令-rename
    @commands.command(pass_context=True)
    @commands.has_permissions(administrator=True)
    async def rename(self, ctx, member: discord.Member, *,name):
        await ctx.message.delete()
        await member.edit(nick=name)
        await ctx.send(f'『更改名稱』**{member.name}** 的暱稱已被變更為: **"{name}"** ')

def setup(bot):
    bot.add_cog(Main(bot))