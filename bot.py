#導入 模組
import discord  #導入Discord.py的專案
from discord.ext import commands  #導入指令
import json  #導入json的檔案形式

#讀取setting.json檔案
with open('setting.json','r', encoding='utf8') as jfile:
    jdata = json.load(jfile)

#甚麼東西=甚麼
client = discord.Client()
bot = commands.Bot(command_prefix='[')

#控制台-機器人上線
@client.event
async def on_ready():
    print('>> [ {0.user} ] 機器人 上線了'.format(client))

#伺服器通知-有人加入了伺服器
@client.event
async def on_member_join(member):
    print(jdata['join_message'])
    channel = client.get_channel(int(jdata['member_join_channel']))
    await channel.send()

#伺服器通知-有人退出了伺服器
@client.event
async def on_member_remove(member):
    print(F'> [ {member} ] 退出了伺服器')
    channel = client.get_channel(int(jdata['member_leave_channel']))
    await channel.send(jdata['leave_message'])

#指令

#指令-Ping 延遲
@bot.command()
async def ping(ctx):
    print(F'> [ {member} ] 打入了 [ping] 指令')
    await ctx.send(F'{round(bot.latency*1000)} 毫秒(ms)')

#指令-Minecraft 你是說Minecraft這款遊戲嗎?
@bot.command()
async def Minecraft(ctx):
    print(F'> [ {member} ] 打入了 [Minecraft] 指令')
    pic = discord.File('C:\\Users\\Taiwan\\Documents\\GitHub\\TaiwanMC_littlelove\Photo\\4GNJ.png')
    await ctx.send('你是說這個遊戲嗎?')

#訊息對話
@client.event
async def on_message(message):
    if message.author == client.user:
        return
#早安
    if message.content.startswith('早安'):
        await message.channel.send('早安! 祝你有個美好的一天!')
#晚安
    if message.content.startswith('晚安'):
        await message.channel.send('晚安! 祝你有個好夢!')
#北七是誰
    if message.content.startswith('北七是誰'):
        await message.channel.send('我不是.... 不要大家都看著我.... 我很害羞')

#Token-金鑰(setting.json)
client.run(jdata['Token'])