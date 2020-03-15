#導入 模組
import discord  #導入Discord.py的專案
from discord.ext import commands  #導入指令
import json, asyncio
import os #導入os模組

#讀取setting.json檔案
with open('setting.json','r', encoding='utf8') as jfile:
    jdata = json.load(jfile)

#甚麼東西=甚麼
bot = commands.Bot(command_prefix="|")
bot.remove_command('help')

#機器人上線
@bot.event
async def on_ready():
    print('《 TaiwanMC-苦力怕同學 》機器人 上線了')
    await bot.change_presence(status=discord.Status.online, activity=discord.Game('|help 獲取指令提示幫助'))
    channel = bot.get_channel(int(jdata['bot_ready_channel']))
    await channel.send("《 **__TaiwanMC-苦力怕同學__** 》上線了")

#錯誤通知
'''@bot.event
async def on_command_error(ctx, error):
    if isinstance(error,commands.CommandNotFound):
        await ctx.message.delete()
        await ctx.send(f'【錯誤】**{ctx.author.mention}** 您輸入了從來沒有在這世界的指令!')
        print(F'【指令】{ctx.author}  輸入了從來沒有在這世界的指令')
        await asyncio.sleep(3)
        await ctx.channel.purge(limit=1)
    elif isinstance(error,commands.MissingPermissions):
        await ctx.message.delete()
        await ctx.send(f'【錯誤】**{ctx.author.mention}** 您沒有權限執行該命令!')
        print(F'【指令】{ctx.author} 執行了一個他沒有權限執行的指令')
        await asyncio.sleep(3)
        await ctx.channel.purge(limit=1)
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.message.delete()
        await ctx.send(f'【錯誤】**{ctx.author.mention}** 此指令需要一個參數!')
        print(F'【指令】{ctx.author}  未輸入指令需要的參數')
        await asyncio.sleep(3)
        await ctx.channel.purge(limit=1)
    else:
        await ctx.message.delete()
        await ctx.send(F'【錯誤】**{ctx.author.mention}** 發生了一個未知的錯誤! 請在試一次!')
        print(F'【指令】{ctx.author}  讓指令發生了未知的錯誤')
        await asyncio.sleep(3)
        await ctx.channel.purge(limit=1)'''

#指令
#指令-invite
@bot.command()
@commands.is_owner()
async def invite(ctx):
    print(F'〔{ctx.author}〕 輸入 [機器人邀請碼] 指令')
    await ctx.message.delete()
    await ctx.send("機器人的邀請碼:https://discordapp.com/api/oauth2/authorize?client_id=563233382478249985&permissions=8&scope=bot")
    await asyncio.sleep(3)
    await ctx.channel.purge(limit=1)

#指令-load
@bot.command()
@commands.is_owner()
async def load(ctx, Exception):
    print(F'〔{ctx.author}〕 輸入 [載入 {Exception}] 指令')
    await ctx.message.delete()
    bot.load_extension(F'{Exception}')
    await ctx.send(F'載入 **{Exception}** 完成!')
    await asyncio.sleep(3)
    await ctx.channel.purge(limit=1)

#指令-unload
@bot.command()
@commands.is_owner()
async def unload(ctx, Exception):
    print(F'〔{ctx.author}〕 輸入 [卸載 {Exception}] 指令')
    await ctx.message.delete()
    bot.unload_extension(F'{Exception}')
    await ctx.send(F'卸載 **{Exception}** 完成!')
    await asyncio.sleep(3)
    await ctx.channel.purge(limit=1)

#指令-reload
@bot.command()
@commands.is_owner()
async def reload(ctx, Exception):
    print(F'〔{ctx.author}〕 輸入 [重新載入 {Exception}] 指令')
    await ctx.message.delete()
    bot.reload_extension(F'{Exception}')
    await ctx.send(F'重新載入 **{Exception}** 完成!')
    await asyncio.sleep(3)
    await ctx.channel.purge(limit=1)

#指令-reload_all
@bot.command()
@commands.is_owner()
async def reload_all(ctx):
    print(F'〔{ctx.author}〕 輸入 [重新載入 全部] 指令')
    await ctx.message.delete()
    bot.reload_extension('cmds.Main')
    bot.reload_extension('cmds.Time_message')
    bot.reload_extension('cmds.Message')
    bot.reload_extension('cmds.Status')
    bot.reload_extension('cmds.Music')
    bot.reload_extension('cmds.Channel')
    bot.reload_extension('event.Msg')
    bot.reload_extension('event.Member')
    await ctx.send(F'重新載入 **全部** 完成!')
    await asyncio.sleep(3)
    await ctx.channel.purge(limit=1)

#導入指令- cmds
for Filename in os.listdir('./cmds'):
    if Filename.endswith('.py'):
        bot.load_extension(F'cmds.{Filename[:-3]}')

#導入指令- event
for Filename in os.listdir('./event'):
    if Filename.endswith('.py'):
        bot.load_extension(F'event.{Filename[:-3]}')

if __name__ == "__main__":
    #Token-金鑰(setting.json)
    bot.run(jdata['Token'])

