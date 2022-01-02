import discord
from discord.ext import commands
import UserData
import asyncio
import os
import random as rand


#PATHS
PIZZA_IMG = os.path.abspath("res/pizza/img/")
PIZZA_SND = os.path.abspath("res/pizza/snd/")


class BoissiCog(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    def get_rand_file(self, base_uri):
        flist = list(os.scandir(base_uri))
        r = rand.randrange(0, len(flist))
        return flist[r].path

    async def temp_mute(self, member, time):
        await member.edit(mute=True)
        await asyncio.sleep(time)
        await member.edit(mute=False)

    @commands.command(name='pizzatime', aliases=['pizza', 'dominos'], description="It's pizza time!")
    async def pizza_(self, ctx):
        player = AudioPlayer(self.bot, ctx.channel.guild)
        await ctx.send("It's pizza time!", file=discord.File(self.get_rand_file(PIZZA_IMG)))
        await player.play(self.get_rand_file(PIZZA_SND))


class AudioPlayer :
    __slots__ = ('bot', '_guild', '_channel', '_cog', 'queue', 'over', 'current', 'np', 'volume')

    def __init__(self, bot, guild):
        self.bot = bot
        self._guild = guild
        self.over = asyncio.Event()

    async def play(self, file):
        self.over.clear()
        await self.bot.wait_until_ready()
        self._guild.voice_client.play(discord.FFmpegPCMAudio(source=file), after=lambda _: self.bot.loop.call_soon_threadsafe(self.over.set))
        await self.over.wait()

