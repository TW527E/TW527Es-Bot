#導入 模組
import discord  #導入Discord.py的專案
from discord.ext import commands  #導入指令
from core.classes import Cog_Extension #導入Cog_extension 的定義
from discord.utils import get
from pathlib import Path
import shutil
import youtube_dl
import spotdl
import os
import json

players = {}
queues = {}

class Voice(Cog_Extension):

    #指令-play 播放音樂
    @commands.command(pass_context=True, aliases=['p', 'pla'])
    async def play(self, ctx, url: str):
        print(F'『音樂』〔{ctx.author}〕 輸入 [play - 播放音樂] 指令 連結為:[{url}]')
        channel = ctx.author.voice.channel
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if voice and voice.is_connected():
            print('《語音頻道》已連接')
        else:
            await ctx.send(f'《語音頻道》已加入到 《**{channel}**》')
            await channel.connect()

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
                path = Path(os.path.dirname(os.path.realpath(__file__)))
                main_location = path.parent
                song_path = os.path.abspath(os.path.realpath("Queue") + "\\" + first_file)
                if length != 0:
                    print("『音樂』歌曲已播放完畢 下一首歌繼續\n")
                    print(f"『音樂』還剩下 {still_q}首歌曲在清單裡")
                    song_there = os.path.isfile("song.mp3")
                    if song_there:
                        os.remove("song.mp3")
                    shutil.move(song_path, main_location)
                    for file in os.listdir("./"):
                        if file.endswith(".mp3"):
                            os.rename(file, 'song.mp3')
                            queues[q_num] -= 1

                    voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: check_queue())
                    voice.source = discord.PCMVolumeTransformer(voice.source)
                    with open('setting.json', mode='r', encoding='utf8') as jfile:
                        jdata = json.load(jfile)
                    voice.source.volume = jdata['volume']
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
            Queue_infile = os.path.isdir("./Queue")
            QueueWait_infile = os.path.isdir("./Queue_Wait")
            if Queue_infile is False:
                os.mkdir("Queue")
            if QueueWait_infile is False:
                os.mkdir("Queue_Wait")
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

            queue_path = os.path.abspath(os.path.realpath("Queue_Wait") + f"\%(title)s.%(ext)s")

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
                print("『音樂』正在下載指定音樂(播放清單)的音樂\n")
                await ctx.send("『音樂』:ballot_box:正在下載指定音樂(播放清單)的音樂")
                ydl.download([url])

            for file in os.listdir(os.path.abspath(os.path.realpath("Queue_Wait"))):
                if file.endswith(".mp3"):
                    name = file
                    print(f"『音樂』重新命名檔案: {file}\n")
                    os.rename(F".\Queue_Wait\{file}", F".\Queue\song{q_num}.mp3")

            embed=discord.Embed(title="------------------------------------", color=0x28d252)
            embed.set_author(name="新增音樂至播放清單")
            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/739005886797840385/739459458488598568/658d047ef378c3147a9d8d3a01fef268.png")
            embed.add_field(name="音樂名稱:", value=F"{name[:-4]}", inline=True)
            embed.add_field(name="播放號碼:", value=F"{q_num}", inline=True)
            await ctx.send(embed=embed)
            print(F"『音樂』已加入音樂 排隊中 音樂名稱:{name[:-4]} 排隊號碼為" + str(q_num))
            #print("『音樂』正在嘗試刪除音樂 可是他還在播")
            #await ctx.send(":musical_note:『音樂』正在嘗試刪除音樂 可是他還在播阿!!!")
            return


        Queue_infile = os.path.isdir("./Queue")
        try:
            Queue_folder = "./Queue"
            QueueWait_folder = "./Queue_Wait"
            if Queue_infile is True:
                print("『音樂』刪除舊的播放清單")
                shutil.rmtree(Queue_folder)
            if Queue_infile is True:
                shutil.rmtree(QueueWait_folder)
        except:
            print("『音樂』沒有播放清單")

        await ctx.send(":musical_note:『音樂』正在下載指定音樂(播放清單)的音樂")

        voice = get(self.bot.voice_clients, guild=ctx.guild)

        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'outtmpl': '%(title)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        try:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                print("『音樂』正在下載指定音樂(播放清單)的音樂\n")
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
        with open('setting.json', mode='r', encoding='utf8') as jfile:
            jdata = json.load(jfile)
        voice.source.volume = jdata['volume']
            
        vvolume = jdata['volume']*100

        embed=discord.Embed(title="------------------------------------", color=0x28d252)
        embed.set_author(name="新增音樂")
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/739005886797840385/739459458488598568/658d047ef378c3147a9d8d3a01fef268.png")
        embed.add_field(name="音樂名稱:", value=F"{name[:-4]}", inline=True)
        embed.add_field(name=":loud_sound:目前音量:", value=F"{vvolume}", inline=True)
        await ctx.send(embed=embed)
        print(F"『音樂』目前播放音樂: {name[:-4]} 音量:{vvolume}%")

    #指令-pause 暫停音樂
    @commands.command(pass_context=True, aliases=['pa', 'pau', 'paus'])
    async def pause(self, ctx):

        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_playing():
            print("『音樂』音樂已暫停")
            voice.pause()
            await ctx.send(":musical_note:『音樂』音樂已暫停")
        else:
            print("『音樂』音樂沒再播放 所以無法暫停")
            await ctx.send(":musical_note:『音樂』音樂沒再播放 所以無法暫停")

    #指令-resume 繼續播放
    @commands.command(pass_context=True, aliases=['r', 'res', 'resum'])
    async def resume(self, ctx):

        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_paused():
            print("『音樂』音樂繼續播放")
            voice.resume()
            await ctx.send(":musical_note:『音樂』音樂繼續播放")
        else:
            print("『音樂』沒有音樂已暫停")
            await ctx.send("『音樂』:musical_note:沒有音樂暫停阿!")

    #指令-stop 停止播放音樂
    @commands.command(pass_context=True, aliases=['s', 'sto'])
    async def stop(self, ctx):

        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_playing():
            print("『音樂』音樂已停止播放")
            voice.stop()
            await ctx.send("『音樂』:stop_button:音樂已停止播放")
        else:
            print("『音樂』沒有音樂在播放")
            await ctx.send("『音樂』:octagonal_sign:沒有音樂在播放")
    
    #指令-queue 播放清單
    @commands.command(pass_context=True, aliases=['q', 'que'])
    async def queue(self, ctx, url: str):
        Queue_infile = os.path.isdir("./Queue")
        QueueWait_infile = os.path.isdir("./Queue_Wait")
        if Queue_infile is False:
            os.mkdir("Queue")
        if QueueWait_infile is False:
            os.mkdir("Queue_Wait")
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

        queue_path = os.path.abspath(os.path.realpath("Queue_Wait") + f"\%(title)s.%(ext)s")

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
            print("『音樂』正在下載指定音樂(播放清單)的音樂\n")
            await ctx.send("『音樂』:ballot_box:正在下載指定音樂(播放清單)的音樂")
            ydl.download([url])

        for file in os.listdir(os.path.abspath(os.path.realpath("Queue_Wait"))):
            if file.endswith(".mp3"):
                name = file
                print(f"『音樂』重新命名檔案: {file}\n")
                os.rename(F".\Queue_Wait\{file}", F".\Queue\song{q_num}.mp3")

        embed=discord.Embed(title="------------------------------------", color=0x28d252)
        embed.set_author(name="新增音樂至播放清單")
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/739005886797840385/739459458488598568/658d047ef378c3147a9d8d3a01fef268.png")
        embed.add_field(name="音樂名稱:", value=F"{name[:-4]}", inline=True)
        embed.add_field(name="播放號碼:", value=F"{q_num}", inline=True)
        await ctx.send(embed=embed)
        print(F"『音樂』已加入音樂 排隊中 音樂名稱:{name[:-4]} 排隊號碼為" + str(q_num))

    #指令-volume 音量
    @commands.command(pass_context=True, aliases=['v', 'vol', 'volum', 'V', 'Vol', 'Volum', 'Volume'])
    async def volume(self, ctx, volume: int):
        if volume <= 100 and volume >= 0:

            if ctx.voice_client is None:
                return await ctx.send("『音樂』:octagonal_sign:還沒還沒有音樂在播放")

            print(F'『音樂』"{ctx.author.name}" 輸入了 指令"Volume" 音量:{str(volume)}')
            with open('setting.json', mode='r', encoding='utf8') as jfile:
                jdata = json.load(jfile)
            jdata['volume'] = volume/100
            with open('setting.json', mode='w', encoding='utf8') as jfile:
                json.dump(jdata, jfile, indent=11)

            ctx.voice_client.source.volume = volume/100
            await ctx.send(f"『音樂』:loud_sound:已調整音量為 **`{volume}%`**")
        
        else:
            print(F'『音樂』"{ctx.author.name}"輸入了 指令"Volume" 可是他打入了 {volume}% 等於說他瘋了')
            await ctx.send(f"『音樂』:octagonal_sign:你太超過了喔 **`{volume}%`** 你瘋了?")

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