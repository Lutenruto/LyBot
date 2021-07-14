import discord
from discord.ext import commands
import youtube_dl
import asyncio


def setup(bot):
    bot.add_cog(CogYoutube(bot))


musics = {}
ytdl = youtube_dl.YoutubeDL()


class Video:
    def __init__(self, link):
        video = ytdl.extract_info(link, download=False)
        video_format = video["formats"][0]
        self.url = video["webpage_url"]
        self.stream_url = video_format["url"]


def play_song(client, queue, song, bot):
    source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(song.stream_url
                                                                 , before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"))

    def nextS(_):
        if len(queue) > 0:
            new_song = queue[0]
            del queue[0]
            play_song(client, queue, new_song, bot)
        else:
            asyncio.run_coroutine_threadsafe(client.disconnect(), bot.loop)

    client.play(source, after=nextS)


class CogYoutube(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="leave")
    async def leave(self, ctx):
        client = ctx.guild.voice_client
        await client.disconnect()
        musics[ctx.guild] = []

    @commands.command(name="resume")
    async def resume(self, ctx):
        client = ctx.guild.voice_client
        if client.is_paused():
            client.resume()

    @commands.command(name="pause")
    async def pause(self, ctx):
        client = ctx.guild.voice_client
        if not client.is_paused():
            client.pause()

    @commands.command(name="skip")
    async def skip(self, ctx):
        client = ctx.guild.voice_client
        client.stop()

    @commands.command(name="play")
    async def play(self, ctx, url):
        client = ctx.guild.voice_client

        if client and client.channel:
            video = Video(url)
            musics[ctx.guild].append(video)
        else:
            channel = ctx.author.voice.channel
            video = Video(url)
            musics[ctx.guild] = []
            client = await channel.connect()
            await ctx.send(f"Je lance : {video.url}")
            play_song(client, musics[ctx.guild], video, self.bot)
