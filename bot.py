import discord

client = discord.Client()

@client.event
async def on_ready():
    print('>> [ {0.user} ] 機器人 上線了'.format(client))

@client.event
async def on_member_join(member):
    print(F'> [ {member} ] 加入了伺服器')
    channel = client.get_channel(638710187678629888)
    await channel.send(F'>> {member.mention} << 加入了伺服器')

@client.event
async def on_member_remove(member):
    print(F'> [ {member} ] 退出了伺服器')
    channel = client.get_channel(638710224554819606)
    await channel.send(F'>> {member.mention} << 退出了伺服器')

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

client.run('NTYzMjMzMzgyNDc4MjQ5OTg1.XiPoaw.1SQeC0sVpE2ypxdHu17C-70cl5w')