import discord
from discord.ext import commands
import json

with open('setting.json','r', encoding='utf8') as jfile:
    jdata = json.load(jfile)

client = discord.Client()
bot = commands.Bot(command_prefix='|')

@client.event
async def on_ready():
    print('>> [ {0.user} ] 機器人 上線了'.format(client))

@client.event
async def on_member_join(member):
    print(F'> [ {member} ] 加入了伺服器')
    channel = client.get_channel(int(jdata['member_join_channel']))
    await channel.send(F'>> {member.mention} << 加入了伺服器')

@client.event
async def on_member_remove(member):
    print(F'> [ {member} ] 退出了伺服器')
    channel = client.get_channel(int(jdata['member_leave_channel']))
    await channel.send(F'>> {member.mention} << 退出了伺服器')

@bot.command()
async def ping(ctx):
    await ctx.send(F'{round(bot.latency*1000)} 毫秒')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('早安'):
        await message.channel.send('早安! 祝你有個美好的一天!')
        
    if message.content.startswith('晚安'):
        await message.channel.send('晚安! 祝你有個好夢!')

    if message.content.startswith('北七是誰'):
        await message.channel.send('我不是.... 不要大家都看著我.... 我很害羞')

client.run(jdata['Token'])