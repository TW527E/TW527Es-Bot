#導入 模組
import discord  #導入Discord.py的專案
from discord.ext import commands  #導入指令
from core.classes import Cog_Extension #導入Cog_extension 的定義
import json  #導入json的檔案形式

#讀取setting.json檔案
with open('setting.json','r', encoding='utf8') as jfile:
    jdata = json.load(jfile)

class Vote(Cog_Extension):

    #指令-
    @commands.command()
    async def vote(self, ctx, title, *, vote):
        await ctx.message.delete()
        vvote = vote.rsplit("=")
        embed=discord.Embed(title=title, description="投票↓", color=0x28d252)
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/739774709490516099/742312626981306398/correctmarksuccesstickvalidyesicon-1320167819078544687.png")
        embed.add_field(name=F"反應:regional_indicator_a:", value=F"{vvote[0]}", inline=True)
        rea = 1
        if len(vvote) >= 2:
            embed.add_field(name=F"反應:regional_indicator_b:", value=F"{vvote[1]}", inline=False)
            rea = 2
        if len(vvote) >= 3:
            embed.add_field(name=F"反應:regional_indicator_c:", value=F"{vvote[2]}", inline=True)
            rea = 3
        if len(vvote) >= 4:
            embed.add_field(name=F"反應:regional_indicator_d:", value=F"{vvote[3]}", inline=False)
            rea = 4
        if len(vvote) >= 5:
            embed.add_field(name=F"反應:regional_indicator_e:", value=F"{vvote[4]}", inline=True)
            rea = 5
        if len(vvote) >= 6:
            embed.add_field(name=F"反應:regional_indicator_f:", value=F"{vvote[5]}", inline=False)
            rea = 6
        if len(vvote) >= 7:
            embed.add_field(name=F"反應:regional_indicator_g:", value=F"{vvote[6]}", inline=True)
            rea = 7
        if len(vvote) >= 8:
            embed.add_field(name=F"反應:regional_indicator_h:", value=F"{vvote[7]}", inline=False)
            rea = 8
        if len(vvote) >= 9:
            embed.add_field(name=F"反應:regional_indicator_i:", value=F"{vvote[8]}", inline=True)
            rea = 9
        if len(vvote) >= 10:
            embed.add_field(name=F"反應:regional_indicator_j:", value=F"{vvote[9]}", inline=False)
            rea = 10
        if len(vvote) >= 11:
            embed.add_field(name=F"反應:regional_indicator_k:", value=F"{vvote[10]}", inline=True)
            rea = 11
        if len(vvote) >= 12:
            embed.add_field(name=F"反應:regional_indicator_l:", value=F"{vvote[11]}", inline=False)
            rea = 12
        if len(vvote) >= 13:
            embed.add_field(name=F"反應:regional_indicator_m:", value=F"{vvote[12]}", inline=True)
            rea = 13
        if len(vvote) >= 14:
            embed.add_field(name=F"反應:regional_indicator_n:", value=F"{vvote[13]}", inline=False)
            rea = 14
        if len(vvote) >= 15:
            embed.add_field(name=F"反應:regional_indicator_o:", value=F"{vvote[14]}", inline=True)
            rea = 15
        if len(vvote) >= 16:
            embed.add_field(name=F"反應:regional_indicator_p:", value=F"{vvote[15]}", inline=False)
            rea = 16
        if len(vvote) >= 17:
            embed.add_field(name=F"反應:regional_indicator_q:", value=F"{vvote[16]}", inline=True)
            rea = 17
        if len(vvote) >= 18:
            embed.add_field(name=F"反應:regional_indicator_r:", value=F"{vvote[17]}", inline=False)
            rea = 18
        if len(vvote) >= 19:
            embed.add_field(name=F"反應:regional_indicator_s:", value=F"{vvote[18]}", inline=True)
            rea = 19
        if len(vvote) >= 20:
            embed.add_field(name=F"反應:regional_indicator_t:", value=F"{vvote[19]}", inline=False)
            rea = 20
        Vote_Msg = await ctx.send(embed=embed)
        await Vote_Msg.add_reaction("🇦")
        if rea >= 2:
            await Vote_Msg.add_reaction("🇧")
        if rea >= 3:
            await Vote_Msg.add_reaction("🇨")
        if rea >= 4:
            await Vote_Msg.add_reaction("🇩")
        if rea >= 5:
            await Vote_Msg.add_reaction("🇪")
        if rea >= 6:
            await Vote_Msg.add_reaction("🇫")
        if rea >= 7:
            await Vote_Msg.add_reaction("🇬")
        if rea >= 8:
            await Vote_Msg.add_reaction("🇭")
        if rea >= 9:
            await Vote_Msg.add_reaction("🇮")
        if rea >= 10:
            await Vote_Msg.add_reaction("🇯")
        if rea >= 11:
            await Vote_Msg.add_reaction("🇰")
        if rea >= 12:
            await Vote_Msg.add_reaction("🇱")
        if rea >= 13:
            await Vote_Msg.add_reaction("🇲")
        if rea >= 14:
            await Vote_Msg.add_reaction("🇳")
        if rea >= 15:
            await Vote_Msg.add_reaction("🇴")
        if rea >= 16:
            await Vote_Msg.add_reaction("🇵")
        if rea >= 17:
            await Vote_Msg.add_reaction("🇶")
        if rea >= 18:
            await Vote_Msg.add_reaction("🇷")
        if rea >= 19:
            await Vote_Msg.add_reaction("🇸")
        if rea >= 20:
            await Vote_Msg.add_reaction("🇹")
        
def setup(bot):
    bot.add_cog(Vote(bot))