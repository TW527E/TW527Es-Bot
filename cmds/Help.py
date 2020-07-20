#導入 模組
import discord  #導入Discord.py的專案
from discord.ext import commands  #導入指令
from core.classes import Cog_Extension #導入Cog_extension 的定義

class Help(Cog_Extension):

    #指令-指令幫助
    @commands.command()
    async def help(self, ctx):
        print(F'《指令》〔{ctx.author}〕 輸入 [help 指令提示幫助] 指令')
        await ctx.message.delete()
        embed=discord.Embed(title="TaiwanMC-苦力怕同學", description="指令提示幫助↓", color=0xd08a2b)
        embed.set_thumbnail(url="https://images-na.ssl-images-amazon.com/images/I/31ORJ91xCUL._SY355_.jpg")
        embed.add_field(name="備註1", value="指令前方加上* = 僅擁有*管理者*權限的人可使用指令 不代表管理員可以用", inline=True)
        embed.add_field(name="備註2", value="指令前方加上@ = 僅限 機器人擁有者 也就是寫的人 可以打的指令", inline=False)
        embed.add_field(name="-------------------", value="指令幫助指令", inline=True)
        embed.add_field(name="|help", value="指令提示幫助", inline=False)
        embed.add_field(name="|help1", value="指令提示幫助1", inline=True)
        embed.add_field(name="|help2", value="指令提示幫助2", inline=False)
        embed.add_field(name="-------------------", value="其他指令", inline=True)
        embed.add_field(name="@|invite", value="獲取機器人邀請碼", inline=False)
        await ctx.send(embed=embed)

    #指令-指令幫助1
    @commands.command()
    async def help1(self, ctx):
        print(F'《指令》〔{ctx.author}〕 輸入 [help1 指令提示幫助1] 指令')
        await ctx.message.delete()
        embed=discord.Embed(title="TaiwanMC-苦力怕同學", description="指令提示幫助1↓", color=0xd08a2b)
        embed.set_thumbnail(url="https://images-na.ssl-images-amazon.com/images/I/31ORJ91xCUL._SY355_.jpg")
        embed.add_field(name="備註1", value="指令前方加上* = 僅擁有*管理者*權限的人可使用指令 不代表管理員可以用", inline=False)
        embed.add_field(name="備註2", value="指令前方加上@ = 僅限 機器人擁有者 也就是寫的人 可以打的指令", inline=True)
        embed.add_field(name="-------------------", value="基本指令", inline=False)
        embed.add_field(name="|ping", value="機器人延遲", inline=True)
        embed.add_field(name="*|kick <@使用者>", value="kick user 讓機器人踢出 指定使用者", inline=False)
        embed.add_field(name="*|ban <@使用者>", value="ban user 讓機器人封鎖 指定使用者", inline=True)
        embed.add_field(name="*|unban <使用者>", value="unban user 讓機器人解除封鎖 指令使用者", inline=False)
        embed.add_field(name="-------------------", value="訊息指令", inline=True)
        embed.add_field(name="*|say_msg <訊息內容>", value="say_message 使機器人傳送一則您指令的訊息", inline=False)
        embed.add_field(name="*|del_msg <訊息數量>", value="del_message 刪除指定數量的訊息", inline=True)
        embed.add_field(name="|MC", value="MC img 傳送隨機的 Minecraft 圖片", inline=False)
        embed.add_field(name="|url_img", value="MC img 傳送網路上隨機的 Minecraft 圖片", inline=True)
        embed.add_field(name="|now_time", value="now time 現在時間顯示", inline=False)
        embed.add_field(name="|avatar", value="avatar 顯示指令使用者頭像", inline=True)
        embed.add_field(name="-------------------", value="狀態指令", inline=False)
        embed.add_field(name="@|shutdown", value="shutdown bot 關閉機器人", inline=True)
        embed.add_field(name="@|online", value="online bot 上線機器人", inline=False)
        embed.add_field(name="@|idle", value="idle bot 閒置機器人", inline=True)
        embed.add_field(name="@|dnd", value="dnd bot 勿擾機器人", inline=False)
        embed.add_field(name="-------------------", value="公告指令", inline=True)
        embed.add_field(name="*|set_auto_ch <頻道ID>", value="set auto message channel 設定 發送公告訊息 頻道", inline=False)
        embed.add_field(name="*|set_auto_time <時間>", value="set auto message time 設定 發送公告訊息 的秒數", inline=True)
        await ctx.send(embed=embed)

    #指令-指令幫助2
    @commands.command()
    async def help2(self, ctx):
        print(F'《指令》〔{ctx.author}〕 輸入 [help2 指令提示幫助2] 指令')
        await ctx.message.delete()
        embed=discord.Embed(title="TaiwanMC-苦力怕同學", description="指令提示幫助2↓", color=0xd08a2b)
        embed.set_thumbnail(url="https://images-na.ssl-images-amazon.com/images/I/31ORJ91xCUL._SY355_.jpg")
        embed.add_field(name="備註1", value="指令前方加上* = 僅擁有*管理者*權限的人可使用指令 不代表管理員可以用", inline=True)
        embed.add_field(name="備註2", value="指令前方加上@ = 僅限 機器人擁有者 也就是寫的人 可以打的指令", inline=False)
        embed.add_field(name="-------------------", value="語音頻道指令", inline=True)
        embed.add_field(name="|join", value="Join Voice Channel 加入到語音頻道", inline=False)
        embed.add_field(name="|leave", value="Leave Voice Channel 離開語音頻道", inline=True)
        embed.add_field(name="-------------------", value="語音頻道指令", inline=False)
        embed.add_field(name="*|add_text_ch", value="Create Text Channel 創建文字頻道", inline=True)
        embed.add_field(name="*|add_voice_ch", value="Create Voice Channel 創建語音頻道", inline=False)
        embed.add_field(name="-------------------", value="插件指令", inline=True)
        embed.add_field(name="@|load <插件檔案名>", value="Load plugin 載入插件", inline=False)
        embed.add_field(name="@|unload <插件檔案名>", value="Unload plugin 卸載插件", inline=True)
        embed.add_field(name="@|reload <插件檔案名>", value="Reload plugin 重新載入插件", inline=False)
        embed.add_field(name="@|reload_all", value="Reload all plugin 重新載入所有插件", inline=True)
        embed.add_field(name="-------------------", value="插件", inline=False)
        embed.add_field(name="cmds.Main", value="基本", inline=True)
        embed.add_field(name="cmds.Message", value="訊息", inline=False)
        embed.add_field(name="cmds.Status", value="狀態", inline=True)
        embed.add_field(name="cmds.Time_message", value="公告", inline=False)
        embed.add_field(name="cmds.Channel", value="文字.語音頻道", inline=True)
        embed.add_field(name="cmds.Music", value="音樂", inline=False)
        embed.add_field(name="event.Member", value="成員加入.退出", inline=True)
        embed.add_field(name="event.Msg", value="自動回覆訊息", inline=False)
        embed.add_field(name="cmds.Help", value="指令提示幫助", inline=True)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Help(bot))