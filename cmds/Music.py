#導入 模組
import discord  #導入Discord.py的專案
from discord.ext import commands  #導入指令
from core.classes import Cog_Extension #導入Cog_extension 的定義
import os
import nacl
import youtube_dl


class Music(Cog_Extension):
    
    @commands.command()
    async def play(self, ctx, url: str):

        song_there = os.path.isfile("song.mp3")
        try:
            if song_there:
                os.remove("song.mp3")
                print("《音樂》已刪除舊的音樂檔案")
        except PermissionError:
            print("《音樂》正在嘗試刪除音樂檔案，但音樂正在撥放")
            await ctx.send("《音樂》錯誤:音樂已經在撥放了")
            return

        await ctx.send("《音樂》準備完成!")

        voice = get(self.bot.voice_clients, guild=ctx.guild)

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            print("《音樂》音樂下載中\n")
            ydl.download([url])

        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                name = file
                print(f"重新命名檔案: {file}\n")
                os.rename(file, "song.mp3")

        voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: print("《音樂》音樂播放完畢"))
        voice.source = discord.PCMVolumeTransformer(voice.source)
        voice.source.volume = 0.07

        nname = name.rsplit("-", 2)
        await ctx.send(f"《音樂》播放中: {nname[0]}")
        print("《音樂》播放中\n")

def setup(bot):
    bot.add_cog(Music(bot))