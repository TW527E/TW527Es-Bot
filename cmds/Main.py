#導入 模組
import discord  #導入Discord.py的專案
from discord.ext import commands  #導入指令
from core.classes import Cog_Extension #導入Cog_extension 的定義
import json  #導入json的檔案形式

#讀取setting.json檔案
with open('setting.json','r', encoding='utf8') as jfile:
    jdata = json.load(jfile)

class Main(Cog_Extension):

    @commands.command()
    @commands.is_owner()
    async def aue(self, ctx):
        accept_decline = await ctx.send("Test")
        print(accept_decline)
        
    #指令-cmd 控制台指令
    @commands.command()
    @commands.is_owner()
    async def cmd(self, ctx, *, test):
        import os,traceback
        embed=discord.Embed(title="TaiwanMC-苦力怕同學", description="指令↓", color=0x28d252)
        embed.set_thumbnail(url="https://images-na.ssl-images-amazon.com/images/I/31ORJ91xCUL._SY355_.jpg")
        embed.add_field(name="已輸入以下指令", value=F">{test}", inline=True)
        print(os.system(f"{test}"))
        await ctx.send(embed=embed)

    #指令-Ping 延遲
    @commands.command()
    async def ping(self, ctx):
        print(F'《指令》〔{ctx.author}〕 輸入 [ping 機器人延遲] 指令')
        await ctx.message.delete()
        embed=discord.Embed(title="TaiwanMC-苦力怕同學", description="Ping值↓", color=0x28d252)
        embed.set_thumbnail(url="https://images-na.ssl-images-amazon.com/images/I/31ORJ91xCUL._SY355_.jpg")
        embed.add_field(name="目前Ping值", value=F"{round(self.bot.latency*1000)} 毫秒(ms)", inline=True)
        await ctx.send(embed=embed)

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

    #指令 - rename - 更改指定使用者名稱
    @commands.command(pass_context=True)
    @commands.has_permissions(administrator=True)
    async def rename(self, ctx, member: discord.Member, *,name):
        await ctx.message.delete()
        if str(member) == '【TaiwanMC】苦力怕同學#9375':
            if ctx.message.author.id == int(jdata['Owner_id']):
                await member.edit(nick=name)
                await ctx.send(f'『更改名稱』暱稱已被變更為: **"{name}"** ')
            else:
                await ctx.send(f'『想幹嘛阿』**{ctx.author.mention}** 想幹嘛阿!')
        else:
            await member.edit(nick=name)
            await ctx.send(f'『更改名稱』**{member.name}** 的暱稱已被變更為: **"{name}"** ')
    
    #指令 - nick - 更改自己名稱
    @commands.command()
    async def nick(self, ctx, *,name):
        await ctx.message.delete()
        user = ctx.author.nick
        await ctx.message.author.edit(nick=name)
        embed = discord.Embed(title=F"『更改{ctx.author.name}名稱』", description=F"[點此到達{ctx.author.name}頭像連結](%s)" % ctx.author.avatar_url, color=0xd08a2b)
        embed.set_thumbnail(url=F"{ctx.author.avatar_url}")
        embed.add_field(name="更改前的名稱", value=F"{user}", inline=True)
        embed.add_field(name="更改後的名稱", value=F"{name}", inline=False)
        embed.set_footer(text=F"此指令由 {ctx.author} 輸入 • ", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    #指令 - avatar - 顯示指令使用者頭像
    @commands.command()
    async def avatar(self, ctx, member: discord.Member=None):  
        print(f'【指令】〔{ctx.author}〕 輸入 [avatar]')
        author = ctx.message.author
        await ctx.message.delete()
        if not member:
            member = ctx.message.author
        show_avatar = discord.Embed(title=F"{member}", description="[點此到達頭像連結](%s)" % member.avatar_url, color=0xd08a2b)
        show_avatar.set_image(url="{}".format(member.avatar_url))
        show_avatar.set_footer(text=F"此指令由 {author} 輸入 • ", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=show_avatar)

def setup(bot):
    bot.add_cog(Main(bot))