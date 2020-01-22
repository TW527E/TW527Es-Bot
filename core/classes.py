#導入 模組
import discord  #導入Discord.py的專案
from discord.ext import commands  #導入指令

class Cog_Extension(commands.Cog):
    def __init__(self, bot):
        self.bot = bot