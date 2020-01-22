#導入 模組
import discord  #導入Discord.py的專案
from discord.ext import commands  #導入指令
import json  #導入json的檔案形式
import random #導入random的模組
import os #導入os模組

#讀取setting.json檔案
with open('setting.json','r', encoding='utf8') as jfile:
    jdata = json.load(jfile)

#甚麼東西=甚麼
bot = commands.Bot(command_prefix="|")

#機器人上線
@bot.event
async def on_ready():
    print('>> [ TaiwanMC-苦力怕同學 ] 機器人 上線了')
    await bot.change_presence(status=discord.Status.online, activity=discord.Game('|cmds 獲取指令提示幫助'))
    channel = bot.get_channel(int(jdata['bot_ready_channel']))
    await channel.send(">> **TaiwanMC-苦力怕同學** << 上線了")

#指令
#指令-load
@bot.command()
async def load(ctx, Exception):
    print(F'有人打入了[載入 {Exception}]指令')
    await ctx.message.delete()
    bot.load_extension(F'cmds.{Exception}')
    await ctx.send(F'載入 **{Exception}** 完成!')

#指令-unload
@bot.command()
async def unload(ctx, Exception):
    print(F'有人打入了[卸載 {Exception}]指令')
    await ctx.message.delete()
    bot.unload_extension(F'cmds.{Exception}')
    await ctx.send(F'卸載 **{Exception}** 完成!')

#指令-reload
@bot.command()
async def reload(ctx, Exception):
    print(F'有人打入了[重新載入 {Exception}]指令')
    await ctx.message.delete()
    bot.reload_extension(F'cmds.{Exception}')
    await ctx.send(F'重新載入 **{Exception}** 完成!')

#指令-reload
@bot.command()
async def reload_all(ctx):
    print(F'有人打入了[重新載入 全部]指令')
    await ctx.message.delete()
    bot.reload_extension(F'cmds')
    await ctx.send(F'重新載入 **全部** 完成!')

#導入指令
for Filename in os.listdir('./cmds'):
    if Filename.endswith('.py'):
        bot.load_extension(F'cmds.{Filename[:-3]}')

if __name__ == "__main__":
    #Token-金鑰(setting.json)
    bot.run(jdata['Token'])