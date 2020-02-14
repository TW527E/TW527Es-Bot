#導入 模組
import discord  #導入Discord.py的專案
from discord.ext import commands  #導入指令
from core.classes import Cog_Extension #導入Cog_extension 的定義

class Main(Cog_Extension):

    #指令-指令幫助
    @commands.command()
    async def help(self, ctx):
        print(F'【指令】 {ctx.author} 打了 [help 指令提示幫助] 指令')
        await ctx.message.delete()
        embed=discord.Embed(title="TaiwanMC-苦力怕同學", description="指令提示幫助↓", color=0xd08a2b)
        embed.set_thumbnail(url="https://images-na.ssl-images-amazon.com/images/I/31ORJ91xCUL._SY355_.jpg")
        embed.add_field(name="備註", value="指令前方加上* = 僅擁有*管理者*權限的人可使用指令 不代表管理員可以用", inline=True)
        embed.add_field(name="-------------------", value="基本指令", inline=False)
        embed.add_field(name="|help", value="指令提示幫助", inline=True)
        embed.add_field(name="|ping", value="機器人延遲", inline=False)
        embed.add_field(name="*|kick <@使用者>", value="kick user 讓機器人踢出 指定使用者", inline=True)
        embed.add_field(name="*|ban <@使用者>", value="ban user 讓機器人封鎖 指定使用者", inline=False)
        embed.add_field(name="*|unban <使用者>", value="unban user 讓機器人解除封鎖 指令使用者", inline=True)
        embed.add_field(name="-------------------", value="訊息指令", inline=False)
        embed.add_field(name="*|say_msg <訊息內容>", value="say_message 使機器人傳送一則您指令的訊息", inline=True)
        embed.add_field(name="*|del_msg <訊息數量>", value="del_message 刪除指定數量的訊息", inline=False)
        embed.add_field(name="|MC", value="MC img 傳送隨機的 Minecraft 圖片", inline=True)
        embed.add_field(name="|url_img", value="MC img 傳送網路上隨機的 Minecraft 圖片", inline=False)
        embed.add_field(name="|now_time", value="now time 現在時間顯示", inline=True)
        embed.add_field(name="-------------------", value="狀態指令", inline=False)
        embed.add_field(name="*|shutdown", value="shutdown bot 關閉機器人", inline=True)
        embed.add_field(name="*|online", value="online bot 上線機器人", inline=False)
        embed.add_field(name="*|idle", value="idle bot 閒置機器人", inline=True)
        embed.add_field(name="-------------------", value="公告指令", inline=False)
        embed.add_field(name="*|set_auto_ch <頻道ID>", value="set auto message channel 設定 發送公告訊息 頻道", inline=True)
        embed.add_field(name="*|set_auto_time <秒數>", value="set auto message time 設定 發送公告訊息 的秒數", inline=False)
        embed.add_field(name="-------------------", value="插件指令", inline=True)
        embed.add_field(name="*|load <插件檔案名>", value="Load plugin 載入插件", inline=False)
        embed.add_field(name="*|unload <插件檔案名>", value="Unload plugin 卸載插件", inline=True)
        embed.add_field(name="*|reload <插件檔案名>", value="Reload plugin 重新載入插件", inline=False)
        embed.add_field(name="*|reload_all", value="Reload all plugin 重新載入所有插件", inline=True)
        await ctx.send(embed=embed)
    

    #指令-Ping 延遲
    @commands.command()
    async def ping(self, ctx):
        print(F'【指令】 {ctx.author} 打了 [ping 機器人延遲] 指令')
        await ctx.message.delete()
        await ctx.send(F'{round(self.bot.latency*1000)} 毫秒(ms)')

    #指令-kick 踢人
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def kick(self, ctx, member : discord.Member, *, reason=None):
        await ctx.message.delete()
        await member.kick(reason=reason)
        print(F'【指令】 {ctx.author} 打了 [kick {member}] 指令')
        await ctx.send(F'使用者 **{member}** 已被踢出')

    #指令-Ban 封鎖
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def ban(self, ctx, member : discord.Member, *, reason=None):
        await ctx.message.delete()
        await member.ban(reason=reason)
        print(F'【指令】 {ctx.author} 打了 [ban {member.name}] 指令')
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
                print(F'【指令】 {ctx.author} 打了 [unban {user}] 指令')
                await ctx.send(F'使用者 >>**{user}**<< 已經解除封鎖')
                return

    #指令-shutdown 下線
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def shutdown(self, ctx):
        print(F'【指令】 {ctx.author} 打了 [shutdown - 機器人關機] 指令')
        await ctx.message.delete()
        await ctx.send('【狀態】掰掰 我已關機')
        await self.bot.change_presence(status=discord.Status.offline)

    #指令-online 上線
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def online(self, ctx):
        print(F'【指令】 {ctx.author} 打了 [online - 機器人上線] 指令')
        await ctx.message.delete()
        await ctx.send('【狀態】你好 我已經啟動!')
        await self.bot.change_presence(status=discord.Status.online, activity=discord.Game('|cmds 獲取指令提示幫助'))

    #指令-idle 
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def idle(self, ctx):
        print(F'【指令】 {ctx.author} 打了 [idle - 機器人閒置] 指令')
        await ctx.message.delete()
        await ctx.send('【狀態】我太懶了 不想做事!')
        await self.bot.change_presence(status=discord.Status.idle, activity=discord.Game('ヾ(≧ ▽ ≦)ゝ'))




def setup(bot):
    bot.add_cog(Main(bot))