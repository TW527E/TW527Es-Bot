#導入 模組
import discord  #導入Discord.py的專案
from discord.ext import commands  #導入指令
from core.classes import Cog_Extension #導入Cog_extension 的定義
from discord.utils import get
import os
import json
import datetime
from pathlib import Path
import shutil
import youtube_dl
import moviepy
import moviepy.editor

players = {}
queues = []

class Voice(Cog_Extension):
    

    #指令-play 播放音樂
    @commands.command(pass_context=True, aliases=['p', 'pla'])
    async def play(self, ctx, *, url: str):
        print(F'『音樂』〔{ctx.author}〕 輸入 [play - 播放音樂] 指令 [{url}]')
        name = ''
        channel = ctx.author.voice.channel
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if voice and voice.is_connected():
            print('《語音頻道》已連接')
        else:
            await ctx.send(f'《語音頻道》已加入到 《**{channel}**》')
            await channel.connect()
        def is_supported(url):
            extractors = youtube_dl.extractor.gen_extractors()
            for e in extractors:
                if e.suitable(url) and e.IE_NAME != 'generic':
                    return True
            return False
        def check_queue():
            queues.append([url, ctx.author.id])
            if len(queues) > 1:
                ctx.send('《音樂》已加入播放清單')
            else:
                ctx.send('《音樂》已加入播放清單，請等待播放')
        if is_supported(url):
            if not voice:
                await ctx.send('《音樂》已加入到播放清單')
                check_queue()
            else:
                if voice.is_playing():
                    await ctx.send('《音樂》已加入到播放清單')
                    check_queue()
                else:
                    ctx.send('《音樂》已加入到播放清單')
                    check_queue()
        else:
            ctx.send('《音樂》檔案格式不支援')
        
        try:
            if len(queues) > 1:
                queues.clear()
                print("『音樂』刪除舊的音樂列表")
        except PermissionError:
            ydl_opts = {
                'format': 'bestaudio/best',
                'extractaudio': True,
                'audioformat': 'mp3',
                'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
                'restrictfilenames': True,
                'noplaylist': True,
                'nocheckcertificate': True,
                'ignoreerrors': False,
                'logtostderr': False,
                'quiet': True,
                'no_warnings': True,
                'default_search': 'auto',
                'source_address': '0.0.0.0',
            }
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                print("『音樂』正在下載指定音樂(播放清單)的音樂\n")
                message = await ctx.send(":musical_note:『音樂』正在下載指定音樂(播放清單)的音樂")
                if is_supported(url) == False:
                    song_search = " ".join(url)
                    ydl.download([f"ytsearch1:{song_search}"])
                else:
                    ydl.download([url])

            for file in os.listdir(os.path.abspath(os.path.realpath("Queue_Wait"))):
                if file.endswith(".mp3"):
                    name = file
                    print(f"『音樂』重新命名檔案: {file}\n")
                    os.rename(F".\Queue_Wait\{file}", F".\Queue\song{q_num}.mp3")

            if is_supported(url) == True:
                ytdl = ydl.extract_info(url, download=False)
                ytid = ytdl.get("id", None)
                ytitle = ytdl.get('title', None)
            
            if is_supported(url) == True:
                embed=discord.Embed(title="------------------------------------", color=0x28d252)
            else:
                embed=discord.Embed(title="------------------------------------", description="(搜尋功能測試中)", color=0x28d252)
            embed.set_author(name="新增音樂")
            if is_supported(url) == True:
                embed.set_thumbnail(url=F"http://img.youtube.com/vi/{ytid}/0.jpg")
            else:
                embed.set_thumbnail(url=F"https://cdn.discordapp.com/attachments/739005886797840385/739459458488598568/658d047ef378c3147a9d8d3a01fef268.png")
            if is_supported(url) == True:
                embed.add_field(name="音樂名稱:", value=F"```{ytitle}```", inline=True)
            else:
                embed.add_field(name="音樂名稱:", value=F"```{name[:-4]}```\n(搜尋功能測試中)", inline=True)
            def convert_Queue(seconds):
                hours = seconds // 3600
                seconds %= 3600
                mins = seconds // 60
                seconds %= 60
                return hours, mins, seconds
            # Create an object by passing the location as a string
            video = moviepy.editor.AudioFileClip(F".\Queue\song{q_num}.mp3")
            # Contains the duration of the video in terms of seconds
            video_duration = int(video.duration)
            hours, mins, secs = convert_Queue(video_duration)
            if hours == 0:
                print(F'音樂長度 : {mins}分鐘 {secs}秒')
                embed.add_field(name="音樂長度:", value=F"{mins}分鐘 {secs}秒", inline=True)
            else:
                print(F'音樂長度 : {hours}小時 {mins}分鐘 {secs}秒')
                embed.add_field(name="音樂長度:", value=F"{hours}小時 {mins}分鐘 {secs}秒", inline=True)
            embed.add_field(name="播放號碼:", value=F"{q_num}", inline=True)
            embed.set_footer(text=F"此音樂由 {ctx.author} • 新增", icon_url=ctx.author.avatar_url)
            await message.edit(embed=embed, content='')
            if is_supported(url) == True:
                print(F"『音樂』已加入音樂 排隊中 音樂名稱:{ytitle} 排隊號碼為" + str(q_num))
            else:
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

        message = await ctx.send(":musical_note:『音樂』正在下載指定音樂(播放清單)的音樂")

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

        if is_supported(url) == False:
            song_search = " ".join(url)

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            print("『音樂』正在下載指定音樂(播放清單)的音樂\n")
            if is_supported(url) == False:
                ydl.download([f"ytsearch1:{song_search}"])
            else:
                ydl.download([url])

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

        if is_supported(url) == True:
            ytdl = ydl.extract_info(url, download=False)
            ytid = ytdl.get("id", None)
            ytitle = ytdl.get('title', None)

        if is_supported(url) == True:
            embed=discord.Embed(title="------------------------------------", color=0x28d252)
        else:
            embed=discord.Embed(title="------------------------------------", description="(搜尋功能測試中)", color=0x28d252)
        embed.set_author(name="新增音樂")
        if is_supported(url) == True:
            embed.set_thumbnail(url=F"http://img.youtube.com/vi/{ytid}/0.jpg")
        else:
            embed.set_thumbnail(url=F"https://cdn.discordapp.com/attachments/739005886797840385/739459458488598568/658d047ef378c3147a9d8d3a01fef268.png")
        if is_supported(url) == True:
            embed.add_field(name="音樂名稱:", value=F"```{ytitle}```", inline=True)
        else:
            embed.add_field(name="音樂名稱:", value=F"```{name[:-4]}```", inline=True)
        def convert(seconds):
            hours = seconds // 3600
            seconds %= 3600
            mins = seconds // 60
            seconds %= 60
            return hours, mins, seconds
        # Create an object by passing the location as a string
        video = moviepy.editor.AudioFileClip(".\song.mp3")
        # Contains the duration of the video in terms of seconds
        video_duration = int(video.duration)
        hours, mins, secs = convert(video_duration)
        now = str(datetime.datetime.now())
        loc = now.rfind('.')
        nnow = now[:loc]
        if hours == 0:
            print(F'音樂長度 : {mins}分鐘 {secs}秒')
            embed.add_field(name="音樂長度:", value=F"{mins}分鐘 {secs}秒", inline=True)
        else:
            print(F'音樂長度 : {hours}小時 {mins}分鐘 {secs}秒')
            embed.add_field(name="音樂長度:", value=F"{hours}小時 {mins}分鐘 {secs}秒", inline=True)
        embed.add_field(name=":loud_sound:目前音量:", value=F"{vvolume}", inline=False)
        embed.set_footer(text=F"此音樂由 {ctx.author} 新增 • {nnow}", icon_url=ctx.author.avatar_url)
        await message.edit(embed=embed, content='')
        if is_supported(url) == True:
            print(F"『音樂』目前播放音樂: {ytitle} 音量:{vvolume}%")
        else:
            print(F"『音樂』目前播放音樂: {name[:-4]} 音量:{vvolume}%")


    #指令-skip 跳過正在播放的音樂
    @commands.command(pass_context=True, aliases=['s', 'sk'])
    async def skip(self, ctx):
        print(F'『音樂』〔{ctx.author}〕 輸入 [skip - 跳過正在播放的音樂]')
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if voice and voice.is_playing():
            print('《音樂》已跳過')
            voice.stop()
            await ctx.send('《音樂》已跳過')
        else:
            await ctx.send('《音樂》沒有正在播放')

    #指令-pause 暫停正在播放的音樂
    @commands.command(pass_context=True, aliases=['pau'])
    async def pause(self, ctx):
        print(F'『音樂』〔{ctx.author}〕 輸入 [pause - 暫停正在播放的音樂]')
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if voice and voice.is_playing():
            print('《音樂》已暫停')
            voice.pause()
            await ctx.send('《音樂》已暫停')
        else:
            await ctx.send('《音樂》沒有正在播放')

    #指令-resume 重新播放正在暫停的音樂
    @commands.command(pass_context=True, aliases=['res'])
    async def resume(self, ctx):
        print(F'『音樂』〔{ctx.author}〕 輸入 [resume - 重新播放正在暫停的音樂]')
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if voice and voice.is_paused():
            print('《音樂》已重新播放')
            voice.resume()
            await ctx.send('《音樂》已重新播放')
        else:
            await ctx.send('《音樂》沒有正在暫停')

    #指令-stop 停止正在播放的音樂
    @commands.command(pass_context=True, aliases=['sto'])
    async def stop(self, ctx):
        print(F'『音樂』〔{ctx.author}〕 輸入 [stop - 停止正在播放的音樂]')
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        queues = []
        if voice and voice.is_playing():
            print('《音樂》已停止')
            voice.stop()
            await ctx.send('《音樂》已停止')
        else:
            await ctx.send('《音樂》沒有正在播放')

    #指令-queue 查看播放清單
    @commands.command(pass_context=True, aliases=['que'])
    async def queue(self, ctx):
        print(F'『音樂』〔{ctx.author}〕 輸入 [queue - 查看播放清單]')
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        queues = []
        if voice and voice.is_playing():
            queues.append(voice.source.title)
        if len(queues) == 0:
            await ctx.send('《音樂》播放清單為空')
        else:
            await ctx.send('《音樂》播放清單為：\n' + '\n'.join(queues))

    #指令-volume 設定音量
    @commands.command(pass_context=True, aliases=['vol'])
    async def volume(self, ctx, volume: int):
        print(F'『音樂』〔{ctx.author}〕 輸入 [volume - 設定音量]')
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if voice and voice.is_playing():
            print('《音樂》已設定音量')
            voice.source.volume = volume / 100
            await ctx.send('《音樂》已設定音量')
        else:
            await ctx.send('《音樂》沒有正在播放')

    #指令-nowplaying 查看正在播放的音樂
    @commands.command(pass_context=True, aliases=['np'])
    async def nowplaying(self, ctx):
        print(F'『音樂』〔{ctx.author}〕 輸入 [nowplaying - 查看正在播放的音樂]')
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if voice and voice.is_playing():
            print('《音樂》已查看正在播放的音樂')
            await ctx.send('《音樂》正在播放：' + voice.source.title)
        else:
            await ctx.send('《音樂》沒有正在播放')

    #指令-loop 播放清單循環
    @commands.command(pass_context=True, aliases=['loo'])
    async def loop(self, ctx):
        print(F'『音樂』〔{ctx.author}〕 輸入 [loop - 播放清單循環]')
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if voice and voice.is_playing():
            print('《音樂》已設定循環播放')
            voice.source.loop = not voice.source.loop
            await ctx.send('《音樂》已設定循環播放')
        else:
            await ctx.send('《音樂》沒有正在播放')

    #指令-shuffle 播放清單隨機
    @commands.command(pass_context=True, aliases=['shu'])
    async def shuffle(self, ctx):
        print(F'『音樂』〔{ctx.author}〕 輸入 [shuffle - 播放清單隨機]')
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if voice and voice.is_playing():
            print('《音樂》已設定隨機播放')
            voice.source.shuffle = not voice.source.shuffle
            await ctx.send('《音樂》已設定隨機播放')
        else:
            await ctx.send('《音樂》沒有正在播放')


def setup(bot):
    bot.add_cog(Voice(bot))