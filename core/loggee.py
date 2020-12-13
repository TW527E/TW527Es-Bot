#導入 模組
from typing import Text
import discord  #導入Discord.py的專案
from discord.ext import commands  #導入指令
import datetime
import core.globals

class Loggee():
    def __init__(self, text):
        now = str(datetime.datetime.now())
        loc = now.rfind('.')
        nnow = now[:loc]
        core.globals.now()
        with open(F'Log/log.{core.globals.timee}.log', 'a', encoding='utf8') as log:
            print(F'{text}', file=log)
        print(F'[{nnow}]> {text}')