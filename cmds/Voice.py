#導入 模組
import discord  #導入Discord.py的專案
from discord.ext import commands  #導入指令
from core.classes import Cog_Extension #導入Cog_extension 的定義
from discord.utils import get
import youtube_dl
import spotdl
import os

players = {}
queues = {}

class Voice(Cog_Extension):

    #指令-play 播放音樂
    @commands.command(pass_context=True, aliases=['p', 'pla'])
    async def play(self, ctx, url: str):
        
        def check_queue():
            Queue_infile = os.path.isdir("./Queue")
            if Queue_infile is True:
                DIR = os.path.abspath(os.path.realpath("Queue"))
                length = len(os.listdir(DIR))
                still_q = length - 1
                try:
                    first_file = os.listdir(DIR)[0]
                except:
                    print("『音樂』沒有音樂在播放清單(s)\n")
                    queues.clear()
                    return
                main_location = os.path.dirname(os.path.realpath(__file__))
                song_path = os.path.abspath(os.path.realpath("Queue") + "\\" + first_file)
                if length != 0:
                    print("『音樂』歌曲已播放完畢 下一首歌繼續\n")
                    print(f"『音樂』以下歌曲還在清單裡: {still_q}")
                    song_there = os.path.isfile("song.mp3")
                    if song_there:
                        os.remove("song.mp3")
                    os.shutil.move(song_path, main_location)
                    for file in os.listdir("./"):
                        if file.endswith(".mp3"):
                            os.rename(file, 'song.mp3')

                    voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: check_queue())
                    voice.source = discord.PCMVolumeTransformer(voice.source)
                    voice.source.volume = 0.7

                else:
                    queues.clear()
                    return

            else:
                queues.clear()
                print("『音樂』最後一首歌結束前沒有歌曲在排隊\n")



        song_there = os.path.isfile("song.mp3")
        try:
            if song_there:
                os.remove("song.mp3")
                queues.clear()
                print("『音樂』刪除舊的音樂檔案")
        except PermissionError:
            print("『音樂』正在嘗試刪除音樂 可是他還在播")
            await ctx.send("『音樂』正在嘗試刪除音樂 可是他還在播阿!!!")
            return


        Queue_infile = os.path.isdir("./Queue")
        try:
            Queue_folder = "./Queue"
            if Queue_infile is True:
                print("『音樂』刪除舊的播放清單")
                os.shutil.rmtree(Queue_folder)
        except:
            print("『音樂』沒有播放清單")

        await ctx.send("『音樂』音樂下載中")

        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        try:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                print("『音樂』音樂下載中\n")
                ydl.download([url])
        except:
            print("『音樂』錯誤 機器人不支持這個連結 (Spotify 的話是正常的)")
            c_path = os.path.dirname(os.path.realpath(__file__))
            os.system("spotdl -f " + '"' + c_path + '"' + " -s " + url)

        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                name = file
                print(f"『音樂』重新命名檔案: {file}\n")
                os.rename(file, "song.mp3")

        voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: check_queue())
        voice.source = discord.PCMVolumeTransformer(voice.source)
        voice.source.volume = 0.7

        nname = name.rsplit("-", 2)
        await ctx.send(f"『音樂』目前播放音樂: {nname[0]}")
        print(F"『音樂』目前播放音樂: {nname[0]}")

    #指令-pause 暫停音樂
    @commands.command(pass_context=True, aliases=['pa', 'pau', 'paus'])
    async def pause(self, ctx):

        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_playing():
            print("『音樂』音樂已暫停")
            voice.pause()
            await ctx.send("『音樂』音樂已暫停")
        else:
            print("『音樂』音樂沒再播放 所以無法暫停")
            await ctx.send("『音樂』音樂沒再播放 所以無法暫停")

    #指令-resume 繼續播放
    @commands.command(pass_context=True, aliases=['r', 'res', 'resum'])
    async def resume(self, ctx):

        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_paused():
            print("『音樂』音樂繼續播放")
            voice.resume()
            await ctx.send("『音樂』音樂繼續播放")
        else:
            print("『音樂』沒有音樂已暫停")
            await ctx.send("『音樂』沒有音樂已暫停")

    #指令-stop 停止播放音樂
    @commands.command(pass_context=True, aliases=['s', 'sto'])
    async def stop(self, ctx):

        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_playing():
            print("『音樂』音樂已停止播放")
            voice.stop()
            await ctx.send("『音樂』音樂已停止播放")
        else:
            print("『音樂』音樂沒再播放 所以無法停止播放")
            await ctx.send("『音樂』音樂沒再播放 所以無法停止播放")
    
    #指令-queue 播放清單
    @commands.command(pass_context=True, aliases=['q', 'que'])
    async def queue(self, ctx, url: str):
        Queue_infile = os.path.isdir("./Queue")
        if Queue_infile is False:
            os.mkdir("Queue")
        DIR = os.path.abspath(os.path.realpath("Queue"))
        q_num = len(os.listdir(DIR))
        q_num += 1
        add_queue = True
        while add_queue:
            if q_num in queues:
                q_num += 1
            else:
                add_queue = False
                queues[q_num] = q_num

        queue_path = os.path.abspath(os.path.realpath("Queue") + f"\song{q_num}.%(ext)s")

        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'outtmpl': queue_path,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            print("『音樂』正在下載播放清單的音樂\n")
            ydl.download([url])
        await ctx.send("『音樂』已加入音樂" + " + str(q_num) + " + "到播放清單")

        print("『音樂』已加入音樂" + " + str(q_num) + " + "到播放清單\n")

    #指令-volume 音量
    @commands.command(pass_context=True, aliases=['v', 'vol', 'volum'])
    async def volume(self, ctx, volume: int):
        if volume <= 100 and volume >= 0:

            if ctx.voice_client is None:
                return await ctx.send("『音樂』還沒連結到語音頻道")

            print(volume/100)

            ctx.voice_client.source.volume = volume / 100
            await ctx.send(f"『音樂』已調整音量為 {volume}%")
        
        else:
            await ctx.send(f"『音樂』你太超過了喔 {volume}% 你瘋了?")

    #指令-next 
    @commands.command(pass_context=True, aliases=['n', 'nex'])
    async def next(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_playing():
            print("『音樂』播放下一首音樂")
            voice.stop()
            await ctx.send("『音樂』下一首音樂")
        else:
            print("『音樂』沒有音樂再播")
            await ctx.send("『音樂』沒有音樂再播")


def setup(bot):
    bot.add_cog(Voice(bot))