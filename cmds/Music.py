#導入 模組
import discord  #導入Discord.py的專案
from discord.ext import commands  #導入指令
from core.classes import Cog_Extension #導入Cog_extension 的定義
import os
import nacl
import youtube_dl


class Music(Cog_Extension):
    
    @commands.command()
    async def join(self, ctx):
        print(f'《語音頻道》〔{ctx.author}〕 輸入 [join] 使機器人加入頻道')
        channel = ctx.author.voice.channel
        await ctx.message.delete()
        await channel.connect()
        await ctx.send(f'《語音頻道》已加入到 《**{channel}**》')


    @commands.command()
    async def leave(self, ctx):
        print(f'《語音頻道》〔{ctx.author}〕 輸入 [leave] 使機器人退出頻道')
        await ctx.message.delete()
        await ctx.voice_client.disconnect()
        await ctx.send('《語音頻道》已退出 **語音頻道**')

    
    @commands.command()
    async def play(self, ctx, url: str):

        song_there = os.path.isfile("song.mp3")
        try:
            if song_there:
                os.remove("song.mp3")
                print("Removed old song file")
        except PermissionError:
            print("Trying to delete song file, but it's being played")
            await ctx.send("ERROR: Music playing")
            return

        await ctx.send("Getting everything ready now")

        voice = get(bot.voice_clients, guild=ctx.guild)

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            print("Downloading audio now\n")
            ydl.download([url])

        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                name = file
                print(f"Renamed File: {file}\n")
                os.rename(file, "song.mp3")

        voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: print("Song done!"))
        voice.source = discord.PCMVolumeTransformer(voice.source)
        voice.source.volume = 0.07

        nname = name.rsplit("-", 2)
        await ctx.send(f"Playing: {nname[0]}")
        print("playing\n")

def setup(bot):
    bot.add_cog(Music(bot))