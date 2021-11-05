#導入 模組
import discord  #導入Discord.py的專案
from discord.ext import commands  #導入指令
import json, asyncio
import os #導入os模組
import datetime
from core.loggee import Loggee
intents = discord.Intents.all()

#讀取setting.json檔案
with open('setting.json', 'r', encoding='utf8') as jfile:
    jdata = json.load(jfile)

#讀取 servers/taiwanmc.json檔案
with open('servers/taiwanmc.json', 'r', encoding='utf8') as tmc:
    taiwanmc_data = json.load(tmc)

#甚麼東西=甚麼
bot = commands.Bot(command_prefix='|', intents = intents)
bot.remove_command('help')

#機器人上線
@bot.event
async def on_ready():
    counter = 0
    await bot.change_presence(activity=discord.Streaming(name="|help 獲取指令提示幫助", url="https://www.twitch.tv/tw527e"))
    if counter == 0:
        Loggee(f'《 TaiwanMC-苦力怕同學 》機器人 上線了')
        channel = bot.get_channel(int(jdata['bot_ready_channel']))
        await channel.send(F"《 **__TaiwanMC-苦力怕同學__** 》上線了")
        counter = 1

#錯誤通知
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error,commands.CommandNotFound):
        await ctx.message.delete()
        await ctx.send(f'【錯誤】**{ctx.author.mention}** 痾...... 好像沒有這東西喔!')
        Loggee(f'『指令』{ctx.author}  輸入了從來沒有在這世界的指令')
        await asyncio.sleep(3)
        await ctx.channel.purge(limit=1)
    elif isinstance(error,commands.MissingPermissions):
        await ctx.message.delete()
        await ctx.send(f'【錯誤】**{ctx.author.mention}** 你沒權限拉 不要想執行了!')
        Loggee(f'『指令』{ctx.author} 執行了一個他沒有權限執行的指令')
        await asyncio.sleep(3)
        await ctx.channel.purge(limit=1)
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.message.delete()
        await ctx.send(f'【錯誤】**{ctx.author.mention}** 我要吃一個參數!')
        Loggee(f'『指令』{ctx.author}  未輸入指令需要的參數')
        await asyncio.sleep(3)
        await ctx.channel.purge(limit=1)
    else:
        await ctx.message.delete()
        await ctx.send(F'【錯誤】**{ctx.author.mention}** 發生了一個錯誤 可是我不知道發生了甚麼錯誤......')
        Loggee(f'『指令』{ctx.author}  讓指令發生了未知的錯誤')
        await asyncio.sleep(3)
        await ctx.channel.purge(limit=1)

#指令
#指令 - logout - 機器人關機
@bot.command()
@commands.is_owner()
async def logout(ctx):
    Loggee(f'『{ctx.author}』 輸入 機器人關機 Shutdown')
    await ctx.send('『登出』登登登登 (XP登出)')
    await bot.logout()

#指令 - invite - 邀請連結
@bot.command()
@commands.is_owner()
async def invite(ctx):
    Loggee(f'『{ctx.author}』 輸入 [機器人邀請碼] 指令')
    await ctx.message.delete()
    await ctx.send("機器人的邀請碼:https://discordapp.com/api/oauth2/authorize?client_id=563233382478249985&permissions=8&scope=bot")
    await asyncio.sleep(3)
    await ctx.channel.purge(limit=1)

#指令 - load - 載入Cog
@bot.command()
@commands.is_owner()
async def load(ctx, Exception):
    Loggee(f'『{ctx.author}』 輸入 [載入 {Exception}] 指令')
    await ctx.message.delete()
    bot.load_extension(F'{Exception}')
    await ctx.send(F'載入 **{Exception}** 完成!')
    await asyncio.sleep(3)
    await ctx.channel.purge(limit=1)

#指令 - unload - 卸載Cog
@bot.command()
@commands.is_owner()
async def unload(ctx, Exception):
    Loggee(f'『{ctx.author}』 輸入 [卸載 {Exception}] 指令')
    await ctx.message.delete()
    bot.unload_extension(F'{Exception}')
    await ctx.send(F'卸載 **{Exception}** 完成!')
    await asyncio.sleep(3)
    await ctx.channel.purge(limit=1)

#指令 - reload - 重新載入Cog
@bot.command()
@commands.is_owner()
async def reload(ctx, Exception):
    Loggee(F'『{ctx.author}』 輸入 [重新載入 {Exception}] 指令')
    await ctx.message.delete()
    bot.reload_extension(F'{Exception}')
    await ctx.send(F'重新載入 **{Exception}** 完成!')
    await asyncio.sleep(3)
    await ctx.channel.purge(limit=1)

#指令 - reload_all - 重新載入全部Cog
@bot.command()
@commands.is_owner()
async def reload_all(ctx):
    Loggee(F'〔{ctx.author}〕 輸入 [重新載入 全部] 指令')
    await ctx.message.delete()
    bot.reload_extension('cmds.Main')
    bot.reload_extension('cmds.Time_message')
    bot.reload_extension('cmds.Voice')
    bot.reload_extension('cmds.Message')
    bot.reload_extension('cmds.Status')
    bot.reload_extension('cmds.Music')
    bot.reload_extension('cmds.Channel')
    bot.reload_extension('cmds.Help')
    bot.reload_extension('cmds.Server')
    bot.reload_extension('event.Msg')
    bot.reload_extension('event.Member')
    bot.reload_extension('cmds.Photo')
    await ctx.send(F'重新載入 **全部** 完成!')
    await asyncio.sleep(3)
    await ctx.channel.purge(limit=1)

#導入Cog - cmds
for Filename in os.listdir('./cmds'):
    if Filename.endswith('.py'):
        bot.load_extension(F'cmds.{Filename[:-3]}')

#導入Cog - event
for Filename in os.listdir('./event'):
    if Filename.endswith('.py'):
        bot.load_extension(F'event.{Filename[:-3]}')

#導入Cog - server 
for Filename in os.listdir('./server'):
    if Filename.endswith('.py'):
        bot.load_extension(F'server.{Filename[:-3]}')

if __name__ == "__main__":
    #Token-金鑰(setting.json)
    bot.run(jdata['Token'])